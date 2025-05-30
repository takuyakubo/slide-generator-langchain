from typing import Any, Dict, List

from pydantic import Field

from core.graphs.states import NodeState


class SlideGenerationState(NodeState):
    images: List[Any] = Field(default=[])  # 画像のリスト
    instruction: str = Field(default="")  # ユーザーからの指示
    image_content: List[Dict[str, Any]] = Field(default=[])  # 画像分析結果
    content_structure: str = Field(default="")  # 構造化されたコンテンツ
    slide_outline: str = Field(default="")  # スライドのアウトライン
    slide_presentation: str = Field(default="")  # 詳細なスライドプレゼンテーション
    html_output: str = Field(default="")  # 最終的なHTML出力
    html_template: str = Field(default="default.html")  # template htmlの名前
