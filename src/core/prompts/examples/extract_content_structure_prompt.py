from langchain_core.messages import HumanMessage, SystemMessage
from llm.providers import ProviderType
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
extract_content_structure_prompt[ProviderType.GOOGLE.value] = content
