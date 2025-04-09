from PIL import Image
import base64
import io

from prompts import get_process_image_prompt
from prompts import get_extract_content_structure_prompt
from prompts import get_generate_slide_outline_prompt
from prompts import get_generate_detailed_slides_prompt
from prompts import get_generate_html_slides_prompt

from workflow_base import LangGraphNode
from workflow_states import SlideGenerationState

from templates import get_template


class ProcessImages(LangGraphNode[SlideGenerationState]):
    name = "process images"
    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """複数の画像を処理して内容を抽出"""
        if state.images == []:
            raise Exception("画像が提供されていません")
        
        # 画像の読み込みと処理
        images = state.images
                    
        all_image_content = []
        
        # 複数画像の処理
        for idx, image in enumerate(images):
            # 画像をbase64エンコード
            if isinstance(image, str):  # 画像がパスとして提供された場合
                with open(image, "rb") as img_file:
                    img_data = base64.b64encode(img_file.read()).decode('utf-8')
            elif isinstance(image, Image.Image):  # PILイメージの場合
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
            else:
                raise Exception(f"サポートされていない画像形式です (画像 {idx+1})")
            
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

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """命令と画像分析結果から構造を抽出"""
        if state.instruction == "":
            raise Exception("命令が提供されていません")
        
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
    def proc(self, state: SlideGenerationState) -> SlideGenerationState:

        prompt = get_generate_html_slides_prompt(
            state.slide_presentation,
            get_template("default.html")
            )
        
        chain = prompt | self.llm
        response = chain.invoke({})
        state.html_output = response.content
        return state
