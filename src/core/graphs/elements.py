import logging
from typing import Callable, Generic, Tuple, TypeVar

from langgraph.graph import END

from config import DEBUG_MODE
from core.graphs.states import NodeState

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="NodeState")


class LangGraphNode(Generic[T]):
    name: str = "to be setup"

    def __init__(self, llm) -> None:
        self.llm = llm

    def action(self, state: T) -> T:
        try:
            self.validate(state)
            logger.info(f"{self.name} starts")
            state_ = self.proc(state)
            logger.info(f"{self.name} ends")
            return state_
        except Exception as e:
            if DEBUG_MODE:
                raise e
            return state.emit_error(f"An error occured during {self.name}: {str(e)}")

    def proc(self, state: T) -> T:
        pass

    def validate(self, state: T) -> None:
        pass

    def generate_node(self) -> Tuple[str, Callable[[T], T]]:
        return self.node_name, self.action

    @property
    def node_name(cls) -> str:
        return cls.name.replace(" ", "_")


class LangGraphConditionalEdge:
    def __init__(self, src: LangGraphNode, tgt: LangGraphNode):
        self.source = src
        self.target = tgt

    @staticmethod
    def check_error(state: NodeState) -> str:
        """エラーがあるかどうかをチェックし、次のステップを決定する"""
        if state.error != "":
            return "error"
        return "continue"

    def args_conditional_edge(self):
        return (
            self.source.node_name,
            self.check_error,
            {"error": END, "continue": self.target.node_name},
        )
