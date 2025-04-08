# 📊 Slide Generator

LangChainとLangGraphを使用して画像や文書からスライドプレゼンテーションを自動生成するツールです。

## 📋 概要

このプロジェクトは、画像データや文書（PDF、HTML形式）を分析し、その内容に基づいて構造化されたHTML形式のスライドプレゼンテーションを自動生成します。LangChainのドキュメント処理機能とLangGraphのワークフロー管理機能を組み合わせて、効率的かつカスタマイズ可能なパイプラインを実現します。

## 🌟 主な機能

- **画像分析**: 画像から内容を抽出しスライド生成に活用
- **文書処理**: PDF/HTMLドキュメントの読み込みと前処理（計画中）
- **構造抽出**: 文書や画像の構造と主要コンテンツの自動抽出
- **スライド生成**: アウトラインと詳細コンテンツの自動生成
- **HTML変換**: カスタマイズ可能なHTMLテンプレートを使用したスライド生成
- **インタラクティブ表示**: JavaScript制御によるスライド間の移動機能

## 🛠️ 前提条件

- Python 3.9+
- OpenAI API キーまたはAnthropic API キー（LLMアクセス用）

## 📦 主要な依存関係

- `langchain`：ドキュメント処理および言語モデルとの統合用
- `langgraph`：ワークフロー構築および管理用
- `langchain-anthropic`：Anthropic Claude モデルとの連携用
- `pydantic`：データモデリング用
- `PIL`：画像処理用

## 🚀 使用方法

### インストール

1. リポジトリをクローン
   ```bash
   git clone https://github.com/takuyakubo/slide-generator-langchain.git
   cd slide-generator-langchain
   ```

2. 仮想環境のセットアップと依存関係のインストール
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. 環境変数の設定（.envファイルを作成）
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

### 基本的な使い方

画像からスライドを生成する例:

```python
# 必要なライブラリのインポート
import sys
from pathlib import Path
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv(override=True)

# プロジェクトルートへのパスを追加
root_dir = Path().absolute().parent
sys.path.append(str(root_dir))

from src.workflow import create_slide_generation_workflow

# ワークフローアプリケーションの作成
app = create_slide_generation_workflow()

# スライド生成の実行
result = app.invoke({
    "images": [
        "/path/to/your/image1.png",
        "/path/to/your/image2.png",
        "/path/to/your/image3.png"
    ],
    "instruction": "これらの画像をもとに、勉強会用のスライドを作成してください。"
})

# 生成されたHTMLの取得
html_output = result["html_output"]

# HTMLを保存
with open("generated_slides.html", "w") as f:
    f.write(html_output)
```

### カスタマイズオプション

- 異なるLLMプロバイダー：現在はAnthropicのClaudeモデルを使用していますが、OpenAIモデルなど他のプロバイダーも使用可能です
- カスタムHTMLテンプレート：独自のHTMLテンプレートを使用してスライドデザインをカスタマイズできます
- 指示の詳細化：`instruction`パラメータを詳細にすることでスライドの内容や方向性を調整できます

## 📂 プロジェクト構造

```
slide-generator-langchain/
│
├── src/                    # ソースコード
│   ├── workflow.py         # メインワークフローの定義
│   ├── workflow_base.py    # ワークフローの基本クラス
│   ├── workflow_nodes.py   # ワークフローのノード（処理ステップ）
│   └── workflow_states.py  # ワークフローの状態管理
│
├── examples/               # 使用例
├── requirements.txt        # 依存関係
├── .env.example            # 環境変数のサンプル
└── README.md               # このファイル
```

## 🔍 処理フロー

1. **画像処理（ProcessImages）**: 入力された画像を分析し、内容を抽出します
2. **構造抽出（ExtractContentStructure）**: 画像分析と指示からスライド構造を特定します
3. **アウトライン生成（GenerateSlideOutline）**: スライドのアウトラインを作成します
4. **詳細化（GenerateDetailedSlides）**: 各スライドの詳細内容を生成します
5. **HTML変換（GenerateHtmlSlides）**: 最終的なHTMLスライドを生成します

## 🔍 今後の改善点

- 複数ファイル形式のサポート（PDF、PPTXなど）
- テキストファイルからのスライド生成
- より洗練されたスライドデザインテンプレート
- 画像の自動挿入と配置
- WebUIの開発

## 🤝 コントリビューション

Issue提出やPull Requestは大歓迎です。大きな変更を加える前には、まずIssueを開いて変更内容について議論してください。

---

**Note**: このプロジェクトは開発段階です。機能や実装が今後も拡張・変更される可能性があります。
