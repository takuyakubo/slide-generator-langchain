from PIL import Image
import base64
import io
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

from workflow_base import LangGraphNode
from workflow_states import SlideGenerationState


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
            
            # 画像分析リクエスト
            image_message = HumanMessage(
                content=[
                    {"type": "text", "text": f"画像 {idx+1}の内容を詳細に分析してください。主要な要素、テキスト、構造を抽出してください。"},
                    {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_data
                    }
                }
                ]
            )
            
            image_analysis = self.llm.invoke([image_message])
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
        
        instruction = state.instruction
        image_content = state.image_content
        
        # 複数画像の分析結果をフォーマット
        image_analyses = "\n\n".join([
            f"画像 {item['image_idx']}の分析結果:\n{item['analysis']}" 
            for item in image_content
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="あなたは与えられた画像分析と命令から、スライド作成に必要な構造を抽出するアシスタントです。"),
            HumanMessage(content=f"""
            画像分析結果：
            {image_analyses}
            
            命令：
            {instruction}
            
            上記の情報から、スライド作成に適した構造を抽出し、以下のフォーマットで出力してください：
            - タイトル
            - サブタイトル
            - 主要なポイント（箇条書き）
            - 結論
            """)
        ])
        
        response = self.llm.invoke(prompt.invoke({}))
        state.content_structure = response.content
        return state

class GenerateSlideOutline(LangGraphNode[SlideGenerationState]):
    name = "generate slide outline"

    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        """抽出された構造からスライドアウトラインを生成"""
        content_structure = state.content_structure
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="あなたはスライドアウトラインを作成するアシスタントです。"),
            HumanMessage(content=f"""
            以下の構造からスライドのアウトラインを作成してください：
            
            {content_structure}
            
            各スライドには以下の情報を含めてください：
            1. スライド番号
            2. タイトル
            3. 主要な内容
            4. 追加すべき視覚的要素の提案
            """)
        ])
        
        response = self.llm.invoke(prompt.invoke({}))
        state.slide_outline = response.content
        return state

class GenerateDetailedSlides(LangGraphNode[SlideGenerationState]):
    name = "generate detailed slides"
    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        slide_outline = state.slide_outline
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="あなたは詳細なスライド内容を生成するアシスタントです。"),
            HumanMessage(content=f"""
            以下のアウトラインから詳細なスライド内容を生成してください：
            
            {slide_outline}
            
            各スライドには以下の情報を含めてください：
            1. スライド番号
            2. タイトル
            3. 内容（完全な文章）
            4. 視覚的要素（図表、画像の説明）
            5. デザインの提案
            
            JSON形式で出力してください。
            """)
        ])
        
        response = self.llm.invoke(prompt.invoke({}))
        state.slide_presentation = response.content
        return state

class GenerateHtmlSlides(LangGraphNode[SlideGenerationState]):
    name = "generate html slides"
    def proc(self, state: SlideGenerationState) -> SlideGenerationState:
        slide_presentation = state.slide_presentation
        
        # HTMLテンプレート
        html_template = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{TITLE}}</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                }
                .slide {
                    width: 100%;
                    height: 100vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    padding: 2rem;
                    box-sizing: border-box;
                }
                .slide-title {
                    font-size: 2.5rem;
                    margin-bottom: 1rem;
                }
                .slide-content {
                    font-size: 1.5rem;
                    max-width: 80%;
                }
                .controls {
                    position: fixed;
                    bottom: 1rem;
                    right: 1rem;
                    display: flex;
                    gap: 0.5rem;
                }
                .controls button {
                    padding: 0.5rem 1rem;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <div id="presentation">
                {{SLIDES}}
            </div>
            
            <div class="controls">
                <button id="prev">前へ</button>
                <button id="next">次へ</button>
            </div>
            
            <script>
                const slides = document.querySelectorAll('.slide');
                let currentSlide = 0;
                
                function showSlide(index) {
                    slides.forEach((slide, i) => {
                        slide.style.display = i === index ? 'flex' : 'none';
                    });
                }
                
                document.getElementById('prev').addEventListener('click', () => {
                    currentSlide = Math.max(0, currentSlide - 1);
                    showSlide(currentSlide);
                });
                
                document.getElementById('next').addEventListener('click', () => {
                    currentSlide = Math.min(slides.length - 1, currentSlide + 1);
                    showSlide(currentSlide);
                });
                
                // 初期表示
                showSlide(currentSlide);
            </script>
        </body>
        </html>
        """
        
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="あなたはスライドデータからHTMLを生成するアシスタントです。"),
            HumanMessage(content=f"""
            以下のスライドデータからHTMLを生成してください：
            
            {slide_presentation}
            
            以下のHTMLテンプレートを使用し、{{TITLE}}をプレゼンテーションのタイトルに、{{SLIDES}}を個々のスライドのHTMLに置き換えてください：
            
            {html_template}
            
            各スライドは<div class="slide">要素として生成し、タイトルは<h1 class="slide-title">、内容は<div class="slide-content">の中に配置してください。
            """)
        ])
        
        response = self.llm.invoke(prompt.invoke({}))
        state.html_output = response.content
        return state
