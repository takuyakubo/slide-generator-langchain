from langchain_core.messages import HumanMessage, SystemMessage

from prompts.key_logics import model_key_logic
from prompts.managers import PromptManager

extract_content_structure_prompt = PromptManager("extract_content_structure_prompt")
content = [
    SystemMessage(
        content="あなたは与えられた画像分析と命令から、スライド作成に必要な構造を抽出するアシスタントです。"
    ),
    HumanMessage(
        content="""
            画像分析結果：
            {image_analyses}
            
            命令：
            {instruction}
            
            上記の情報から、スライド作成に適した構造を抽出し、以下のフォーマットで出力してください：
            - タイトル
            - サブタイトル
            - 主要なポイント（箇条書き）
            - 結論
            """
    ),
]
extract_content_structure_prompt["gemini"] = content
extract_content_structure_prompt["claude"] = content
extract_content_structure_prompt["gpt"] = content
extract_content_structure_prompt.get_item_logic = model_key_logic
