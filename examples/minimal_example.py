"""
最小限の使用例

このスクリプトは、slide-generator-langchainを使用するための
最小限の実装例を示しています。
"""

from dotenv import load_dotenv
from src.workflow import create_slide_generation_workflow

# 環境変数の読み込み
load_dotenv()

# ワークフローの作成
app = create_slide_generation_workflow()

# スライド生成の実行
result = app.invoke({
    "images": [
        # 画像ファイルのパスを指定（実際のパスに変更してください）
        "./examples/images/image1.png",
    ],
    "instruction": "この画像をもとに、技術解説用のスライドを作成してください。"
})

# 生成されたHTMLを保存
with open("slide_output.html", "w", encoding="utf-8") as f:
    f.write(result["html_output"])

print("スライドが生成されました: slide_output.html")
