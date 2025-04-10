from workflow.base import LangGraphNode
from workflow.states import SlideGenerationState

from prompts import (
    extract_content_structure_prompt,
    generate_detailed_slides_prompt,
    generate_html_slides_prompt,
    generate_slide_outline_prompt,
    process_image_prompt,
)
from templates import templates
from utils import image_to_image_data_str


class ProcessImages(LangGraphNode[SlideGenerationState]):
    name = "process images"

    def validate(self, state: SlideGenerationState) -> None:
        if state.images == []:
            raise Exception("画像が提供されていません")

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """複数の画像を処理して内容を抽出"""
        # 画像の読み込みと処理
        images = state.images

        all_image_content = []
        # 複数画像の処理 # TBD 並列化
        for idx, image in enumerate(images):
            img_data = image_to_image_data_str(image)
            prompt = process_image_prompt[self.llm.model](img_data=img_data)
            chain = prompt | self.llm
            image_analysis = chain.invoke({})
            all_image_content.append(
                {"image_idx": idx + 1, "analysis": image_analysis.content}
            )
        state.image_content = all_image_content
        return state


class ExtractContentStructure(LangGraphNode[SlideGenerationState]):
    name = "extract content structure"

    def validate(self, state: SlideGenerationState) -> None:
        if state.instruction == "":
            raise Exception("命令が提供されていません")

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """命令と画像分析結果から構造を抽出"""
        # 複数画像の分析結果をフォーマット
        image_analyses = "\n\n".join(
            [
                f"画像 {item['image_idx']}の分析結果:\n{item['analysis']}"
                for item in state.image_content
            ]
        )

        prompt = extract_content_structure_prompt[self.llm.model](
            image_analyses=image_analyses, instruction=state.instruction
        )
        chain = prompt | self.llm
        response = chain.invoke({})
        state.content_structure = response.content
        return state


class GenerateSlideOutline(LangGraphNode[SlideGenerationState]):
    name = "generate slide outline"

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """抽出された構造からスライドアウトラインを生成"""
        prompt = generate_slide_outline_prompt[self.llm.model](
            content_structure=state.content_structure
        )
        chain = prompt | self.llm
        response = chain.invoke({})
        state.slide_outline = response.content
        return state


class GenerateDetailedSlides(LangGraphNode[SlideGenerationState]):
    name = "generate detailed slides"

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        prompt = generate_detailed_slides_prompt[self.llm.model](
            slide_outline=state.slide_outline
        )
        chain = prompt | self.llm
        response = chain.invoke({})
        state.slide_presentation = response.content
        return state


class GenerateHtmlSlides(LangGraphNode[SlideGenerationState]):
    name = "generate html slides"

    def validate(self, state: SlideGenerationState) -> None:
        templates.check_(state.html_template)

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        prompt = generate_html_slides_prompt[self.llm.model](
            slide_presentation=state.slide_presentation, html_template=templates.content
        )
        chain = prompt | self.llm
        response = chain.invoke({})
        state.html_output = response.content
        return state
