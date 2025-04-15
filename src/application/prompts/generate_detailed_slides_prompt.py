from langchain_core.messages import HumanMessage, SystemMessage

from core.llm.providers import ProviderType
from core.prompts.managers import PromptManager

generate_detailed_slides_prompt = PromptManager("generate_detailed_slides_prompt")
content = [
    SystemMessage(content="あなたは詳細なスライド内容を生成するアシスタントです。"),
    HumanMessage(
        content="""
            以下のアウトラインから詳細なスライド内容を生成してください：
            
            {slide_outline}
            
            各スライドには以下の情報を含めてください：
            1. スライド番号
            2. タイトル
            3. 内容（完全な文章）
            4. 視覚的要素（図表、画像の説明）
            5. デザインの提案
            
            JSON形式で出力してください。
            """
    ),
]
generate_detailed_slides_prompt[ProviderType.GOOGLE.value] = content
