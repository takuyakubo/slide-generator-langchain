from langchain_core.messages import HumanMessage, SystemMessage

from core.llm.providers import ProviderType
from core.prompts.managers import PromptManager

generate_html_slides_prompt = PromptManager("generate_html_slides_prompt")
content = [
    SystemMessage(content="あなたはスライドデータからHTMLを生成するアシスタントです。"),
    HumanMessage(
        content="""
            以下のスライドデータからHTMLを生成してください：
            
            {slide_presentation}
            
            以下のHTMLテンプレートを使用してください：
            
            {html_template}

            【重要】HTMLテンプレート内のCSSクラス名やHTML構造を変更しないでください。特に次の点を厳守してください：
            
            1. slide-title, slide-title-page, note, two-col, col, definition-box などの既存のクラス名は全て厳密に維持すること
            2. CSSの構造やプロパティの変更は禁止されています。
            3. テンプレートに定義されていないクラスの新たな追加は禁止されています。
            4. テンプレートの基本構造（divの入れ子構造など）を維持すること
            
            テンプレートには以下の変数があり、適切に置き換えてください：
            
            1. {{title}} - プレゼンテーションのタイトル
            2. {{subtitle}} - サブタイトル（あれば）
            3. {{date}} - 発表日
            4. {{toc}} - 目次の内容（<li>項目</li>の形式）
            5. {{description}} - プレゼンテーションの概要
            6. {{content_title}} - 各コンテンツセクションのタイトル
            7. {{content}} - 各スライドの本文内容
            8. {{summary}} - まとめの箇条書き（<li>項目</li>の形式）
            9. {{conclusion}} - 結論部分
            10. {{footer}} - フッター情報
            
            生成する際の注意点：
            
            1. スライドの種類に応じて適切なクラスを使用してください：
               - 表紙スライド: slide-title クラスを使用
               - 目次スライド: 箇条書きリスト
               - 通常コンテンツスライド: 適切な見出しレベル(h2, h3)とコンテンツ構造
               - まとめスライド: 箇条書きリスト
               - 区切りスライド（必要な場合）: divider-slide クラスを使用
            
            2. 以下の特殊な要素に対応してください：
               - 数式: MathJaxの構文($...$や$$...$$)を使用
               - 表: <table>要素で適切に構造化
               - 画像への参照: image-container, image-boxクラスを使用
               - 重要な定義: definition-boxクラスを使用
               - 注釈: noteクラスを使用
               - 重要ポイント: key-pointクラスを使用
               - 2カラムレイアウト: two-col, colクラスを使用
            
            3. レスポンシブデザインとプリントに対応するため、CSSクラスを適切に活用してください。
            
            4. 日本語のコンテンツを正しく表示するためにUTF-8エンコーディングが設定されていることを確認してください。
            
            最終的な出力はHTMLのみを提供し、```html```のようなマークダウン記法は使用せず、そのままのHTMLコードを出力してください。
            """
    ),
]
generate_html_slides_prompt[ProviderType.GOOGLE.value] = content
