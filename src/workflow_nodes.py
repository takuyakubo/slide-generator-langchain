from prompts import get_process_image_prompt
from prompts import get_extract_content_structure_prompt
from prompts import get_generate_slide_outline_prompt
from prompts import get_generate_detailed_slides_prompt
from prompts import get_generate_html_slides_prompt

from utils import image_to_image_data_str
from templates import templates

from workflow_base import LangGraphNode
from workflow_states import SlideGenerationState


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
            prompt = get_process_image_prompt(img_data, model=self.llm.model)
            chain = prompt | self.llm
            image_analysis = chain.invoke({})
            all_image_content.append({
                "image_idx": idx+1, 
                "analysis": image_analysis.content
            })
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
        image_analyses = "\n\n".join([
            f"画像 {item['image_idx']}の分析結果:\n{item['analysis']}" 
            for item in state.image_content
        ])
        
        prompt = get_extract_content_structure_prompt(image_analyses, state.instruction)
        chain = prompt | self.llm
        response = chain.invoke({})
        state.content_structure = response.content
        return state

class GenerateSlideOutline(LangGraphNode[SlideGenerationState]):
    name = "generate slide outline"

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """抽出された構造からスライドアウトラインを生成"""
        prompt = get_generate_slide_outline_prompt(state.content_structure)
        chain = prompt | self.llm
        response = chain.invoke({})
        state.slide_outline = response.content
        return state

class GenerateDetailedSlides(LangGraphNode[SlideGenerationState]):
    name = "generate detailed slides"
    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        prompt = get_generate_detailed_slides_prompt(state.slide_outline)
        chain = prompt | self.llm
        response = chain.invoke({})
        state.slide_presentation = response.content
        return state

class GenerateHtmlSlides(LangGraphNode[SlideGenerationState]):
    name = "generate html slides"
    def validate(self, state: SlideGenerationState) -> None:
        templates.check_(state.html_template)
    
    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        prompt = get_generate_html_slides_prompt(
            state.slide_presentation,
            templates.content
            )
        chain = prompt | self.llm
        response = chain.invoke({})
        state.html_output = response.content
        return state
