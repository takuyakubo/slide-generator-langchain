from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

from prompts import (
    extract_content_structure_prompt,
    generate_detailed_slides_prompt,
    generate_html_slides_prompt,
    generate_slide_outline_prompt,
    process_image_prompt,
)
from templates import templates
from utils import image_to_image_data_str
from workflow.base import LangGraphNode
from workflow.states import SlideGenerationState


class ProcessImages(LangGraphNode[SlideGenerationState]):
    name = "process images"

    def validate(self, state: SlideGenerationState) -> None:
        if state.images == []:
            raise Exception("画像が提供されていません")

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """複数の画像を処理して内容を抽出"""
        chain = RunnableLambda(
            lambda x: [
                {"image_idx": idx + 1, "url": image}
                for idx, image in enumerate(x.images)
            ]
        ) | RunnableLambda(  # 画像リストを取得
            (
                RunnablePassthrough.assign(
                    img_data=lambda x: image_to_image_data_str(x["url"])
                )
                | RunnableParallel(
                    image_idx=lambda x: x["image_idx"],
                    analysis=(process_image_prompt[self.llm.model] | self.llm),
                )
            ).batch
        )
        state.image_content = chain.invoke(state)
        return state


class ExtractContentStructure(LangGraphNode[SlideGenerationState]):
    name = "extract content structure"

    def validate(self, state: SlideGenerationState) -> None:
        if state.instruction == "":
            raise Exception("命令が提供されていません")

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """命令と画像分析結果から構造を抽出"""

        # 複数画像の分析結果をフォーマット
        def concat_content(state):
            return "\n\n".join(
                [
                    f"画像 {item['image_idx']}の分析結果:\n{item['analysis']}"
                    for item in state.image_content
                ]
            )

        chain = (
            RunnableParallel(
                image_analyses=concat_content, instruction=lambda x: x.instruction
            )
            | extract_content_structure_prompt[self.llm.model]
            | self.llm
            | StrOutputParser()
        )
        state.content_structure = chain.invoke(state)
        return state


class GenerateSlideOutline(LangGraphNode[SlideGenerationState]):
    name = "generate slide outline"

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """抽出された構造からスライドアウトラインを生成"""
        chain = (
            RunnableLambda(lambda x: {"content_structure": x.content_structure})
            | generate_slide_outline_prompt[self.llm.model]
            | self.llm
            | StrOutputParser()
        )
        state.slide_outline = chain.invoke(state)
        return state


class GenerateDetailedSlides(LangGraphNode[SlideGenerationState]):
    name = "generate detailed slides"

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        chain = (
            RunnableLambda(lambda x: {"slide_outline": x.slide_outline})
            | generate_detailed_slides_prompt[self.llm.model]
            | self.llm
            | StrOutputParser()
        )
        state.slide_presentation = chain.invoke(state)
        return state


class GenerateHtmlSlides(LangGraphNode[SlideGenerationState]):
    name = "generate html slides"

    def validate(self, state: SlideGenerationState) -> None:
        templates.check_(state.html_template)

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        chain = (
            RunnableLambda(
                lambda x: {
                    "slide_presentation": x.slide_presentation,
                    "html_template": templates.content,
                }
            )
            | generate_html_slides_prompt[self.llm.model]
            | self.llm
            | StrOutputParser()  # TBD HTMLだけを抜き出すようなParserを作った方が良い
        )
        state.html_output = chain.invoke(state)
        return state
