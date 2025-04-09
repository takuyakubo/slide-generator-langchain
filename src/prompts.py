from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

def get_process_image_prompt(img_data, model='claude'):
    if model.startswith('claude-'):
        img = {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_data}}
    elif model.startswith('models/gemini-'):
        img = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_data}"}}
    else:
        raise Exception("想定外のモデルが使用されました。画像サポートができません。")

    direction = {"type": "text", "text": "画像の内容を詳細に分析してください。主要な要素、テキスト、構造を抽出してください。"}  
    return ChatPromptTemplate.from_messages([
        HumanMessage(content=[direction, img])
    ])

def get_extract_content_structure_prompt(image_analyses, instruction):
    return ChatPromptTemplate.from_messages([
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

def get_generate_slide_outline_prompt(content_structure):
    return ChatPromptTemplate.from_messages([
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
    
def get_generate_detailed_slides_prompt(slide_outline):
    return ChatPromptTemplate.from_messages([
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

def get_generate_html_slides_prompt(slide_presentation, html_template):
    return ChatPromptTemplate.from_messages([
            SystemMessage(content="あなたはスライドデータからHTMLを生成するアシスタントです。"),
            HumanMessage(content=f"""
            以下のスライドデータからHTMLを生成してください：
            
            {slide_presentation}
            
            以下のHTMLテンプレートを使用し、{{TITLE}}をプレゼンテーションのタイトルに、{{SLIDES}}を個々のスライドのHTMLに置き換えてください：
            
            {html_template}
            
            各スライドは<div class="slide">要素として生成し、タイトルは<h1 class="slide-title">、内容は<div class="slide-content">の中に配置してください。
            """)
        ])