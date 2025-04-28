from langchain_core.messages import HumanMessage, SystemMessage

from core.llm.providers import ProviderType
from core.prompts.managers import PromptManager

generate_comprehensive_slides_prompt = PromptManager("generate_comprehensive_slides_prompt")
content = [
    SystemMessage(content="あなたは詳細なスライド内容を設計・生成するアシスタントです。"),
    HumanMessage(
        content="""
            以下の内容から詳細なスライド内容を生成してください：
            
            {content_structure}
            
            各スライドには以下の情報を必ず含めてください：
            1. スライド番号
            2. タイトル
            3. 主要な内容（完全な文章で）
            4. 視覚的要素（図表、画像の詳細な説明）
            5. デザインの提案（色使い、レイアウト、フォントなど）
            
            情報の流れと一貫性を保ちながら、プレゼンテーション全体が論理的に展開されるようにしてください。
            各スライドは前後のスライドとの関連性を意識し、全体として統一感のあるストーリーを作ってください。
            
            JSON形式で出力してください。
            """
    ),
]
generate_comprehensive_slides_prompt[ProviderType.GOOGLE.value] = content