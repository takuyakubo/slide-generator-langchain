from pydantic import BaseModel, Field


class NodeState(BaseModel):
    error: str = Field(default="")  # エラーメッセージ（存在する場合）

    def emit_error(self, error_str):
        return self.model_copy(update={"error": error_str})
