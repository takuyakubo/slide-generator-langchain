from langchain_core.messages import HumanMessage, SystemMessage

from language_models.providers import ProviderType
from prompts.managers import PromptManager

generate_html_slides_prompt = PromptManager("generate_html_slides_prompt")
content = [
    SystemMessage(content="あなたはスライドデータからHTMLを生成するアシスタントです。"),
    HumanMessage(
        content="""
            以下のスライドデータからHTMLを生成してください：
            
            {slide_presentation}
            
            以下のHTMLテンプレートを使用し、{{TITLE}}をプレゼンテーションのタイトルに、{{SLIDES}}を個々のスライドのHTMLに置き換えてください：
            
            {html_template}
            
            各スライドは<div class="slide">要素として生成し、タイトルは<h1 class="slide-title">、内容は<div class="slide-content">の中に配置してください。
            出力はHTMLのみをそのままするか、文字列を入れたい場合はHTMLと分かるように```HTML ```で囲うようにして下さい。
            """
    ),
]
generate_html_slides_prompt[ProviderType.GOOGLE.value] = content
