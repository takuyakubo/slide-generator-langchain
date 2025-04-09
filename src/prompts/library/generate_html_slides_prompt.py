from langchain_core.messages import HumanMessage, SystemMessage
from prompts.managers import PromptManager
from prompts.key_logics import model_key_logic
generate_html_slides_prompt = PromptManager("generate_html_slides_prompt")
content = [
            SystemMessage(content="あなたはスライドデータからHTMLを生成するアシスタントです。"),
            HumanMessage(content="""
            以下のスライドデータからHTMLを生成してください：
            
            {slide_presentation}
            
            以下のHTMLテンプレートを使用し、{{TITLE}}をプレゼンテーションのタイトルに、{{SLIDES}}を個々のスライドのHTMLに置き換えてください：
            
            {html_template}
            
            各スライドは<div class="slide">要素として生成し、タイトルは<h1 class="slide-title">、内容は<div class="slide-content">の中に配置してください。
            """)
        ]
generate_html_slides_prompt['gemini'] = content
generate_html_slides_prompt['claude'] = content
generate_html_slides_prompt.get_item_logic = model_key_logic