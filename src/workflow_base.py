from langgraph.graph import StateGraph, END, START
from typing import List, Callable, Tuple, TypeVar, Generic
from pydantic import BaseModel, Field

class NodeState(BaseModel):
    error: str  = Field(default="")# エラーメッセージ（存在する場合）

    def emit_error(self, error_str):
        return self.model_copy(update={"error": error_str})

T = TypeVar('T', bound='NodeState')

class LangGraphNode(Generic[T]):
    name: str =  "to be setup"

    def __init__(self, llm) -> None:
        self.llm = llm

    def action(self, state: T) -> T:
        try:
            self.validate(state)
            print(f"{self.name} starts")
            state_ = self.proc(state)
            print(f"{self.name} ends")
            return state_
        except Exception as e:
            return state.emit_error(
                f"An error occured during {self.name}: {str(e)}"
            )

    def proc(self, state: T) -> T:
        pass

    def validate(self, state: T) -> None:
        pass

    def generate_node(self) -> Tuple[str, Callable[[T], T]]:
        return self.node_name(), self.action
    
    @classmethod
    def node_name(cls) -> str:
        return cls.name.replace(' ', '_')
    
class LangGraphConditionalEdge:
    def __init__(self, src:LangGraphNode, tgt:LangGraphNode):
        self.source = src
        self.target = tgt

    @staticmethod
    def check_error(state: NodeState) -> str:
        """エラーがあるかどうかをチェックし、次のステップを決定する"""
        if state.error != "":
            return "error"
        return "continue"
    
    def args_conditional_edge(self):
        return self.source.node_name(), self.check_error, {
            "error": END, "continue": self.target.node_name()
        }

class SequentialWorkflow:
    def __init__(self, nodes:List[LangGraphNode], init_state_cls) -> None:
        self.workflow = StateGraph(init_state_cls)
        self.setup(nodes)
 
    def setup(self, nodes:List[LangGraphNode]) -> None:
        nodes_with_sentinels = [START] + nodes + [END]
        edges = [
            LangGraphConditionalEdge(s, t)
            for s, t in zip(nodes_with_sentinels, nodes_with_sentinels[1:])
            ]
        for e in edges:
            if e.target == END:
                node_name = e.source.node_name()
                self.workflow.add_edge(node_name, END)
                continue
            self.workflow.add_node(*e.target.generate_node())
            if e.source == START:
                self.workflow.set_entry_point(e.target.node_name())
            else:
                self.workflow.add_conditional_edges(*e.args_conditional_edge())


    def get_app(self):
        return self.workflow.compile()
