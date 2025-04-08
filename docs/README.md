# Slide Generator ドキュメント

このディレクトリには、Slide Generatorの包括的なドキュメントが含まれています。

## 目次

1. [チュートリアル](TUTORIAL.md) - 初めての方向けのステップバイステップガイド
2. [使用ガイド](USAGE.md) - 詳細な使用方法と機能説明
3. [APIリファレンス](API_REFERENCE.md) - APIの詳細な説明

## クイックスタート

Slide Generatorを始めるための最も簡単な方法は、以下の手順に従うことです：

```python
from dotenv import load_dotenv
from src.workflow import create_slide_generation_workflow

# 環境変数の読み込み
load_dotenv()

# ワークフローの作成
app = create_slide_generation_workflow()

# スライド生成の実行
result = app.invoke({
    "images": [
        "/path/to/your/image1.png",
        "/path/to/your/image2.png"
    ],
    "instruction": "これらの画像をもとに、技術解説用のスライドを作成してください。"
})

# 生成されたHTMLを保存
with open("generated_slides.html", "w", encoding="utf-8") as f:
    f.write(result["html_output"])
```

詳細な使い方については、[チュートリアル](TUTORIAL.md)を参照してください。

## サンプルコード

完全な使用例は、[examples](../examples)ディレクトリにあります：

- [minimal_example.py](../examples/minimal_example.py) - 最小限の使用例
- [image_to_slide_example.py](../examples/image_to_slide_example.py) - 画像からスライドを生成する詳細な例

## プロジェクト構造

プロジェクトの主要なコンポーネントは以下の通りです：

- `src/` - ソースコード
  - `workflow.py` - メインワークフローの定義
  - `workflow_base.py` - ワークフローの基本クラス
  - `workflow_nodes.py` - ワークフローのノード（処理ステップ）
  - `workflow_states.py` - ワークフローの状態管理
- `examples/` - 使用例
- `docs/` - ドキュメント

## サポート

問題や質問がある場合は、GitHubのIssueを通じてお問い合わせください。
