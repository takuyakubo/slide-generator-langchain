from langchain_core.messages import HumanMessage, SystemMessage

from prompts.key_logics import model_key_logic
from prompts.managers import PromptManager

generate_slide_outline_prompt = PromptManager("generate_slide_outline_prompt")
content = [
    SystemMessage(content="あなたはスライドアウトラインを作成するアシスタントです。"),
    HumanMessage(
        content="""
            以下の構造からスライドのアウトラインを作成してください：
            
            {content_structure}
            
            各スライドには以下の情報を含めてください：
            1. スライド番号
            2. タイトル
            3. 主要な内容
            4. 追加すべき視覚的要素の提案
            """
    ),
]
generate_slide_outline_prompt["gemini"] = content
generate_slide_outline_prompt["claude"] = content
generate_slide_outline_prompt["gpt"] = content
generate_slide_outline_prompt.get_item_logic = model_key_logic
