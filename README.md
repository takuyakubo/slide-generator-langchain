# 📊 Slide Generator

LangChainとLangGraphを使用して画像からスライドプレゼンテーションを自動生成するツールです。

## 📋 概要

このプロジェクトは、画像データを分析し、その内容に基づいて構造化されたHTML形式のスライドプレゼンテーションを自動生成します。LangChainのドキュメント処理機能とLangGraphのワークフロー管理機能を組み合わせて、効率的かつカスタマイズ可能なパイプラインを実現します。

## 🌟 主な機能

- **画像分析**: 画像から内容を抽出しスライド生成に活用
- **構造抽出**: 画像の構造と主要コンテンツの自動抽出
- **スライド生成**: アウトラインと詳細コンテンツの自動生成
- **HTML変換**: カスタマイズ可能なHTMLテンプレートを使用したスライド生成
- **インタラクティブ表示**: JavaScript制御によるスライド間の移動機能

## 🔍 今後の開発予定

- **文書処理**: PDF/HTMLドキュメントの読み込みと前処理
- **テキストファイルからのスライド生成**: テキストファイルからのスライド自動生成
- **WebUIの開発**: 使いやすいウェブインターフェースの追加

## 🛠️ 前提条件

- Python 3.9+
- Google Gemini API キーまたはOpenAI API キー（LLMアクセス用）

## 📦 主要な依存関係

- `langchain`：ドキュメント処理および言語モデルとの統合用
- `langgraph`：ワークフロー構築および管理用
- `langchain-google-genai`：Google Gemini モデルとの連携用
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
   GOOGLE_API_KEY=your_api_key_here
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

from src.application.workflow import create_slide_generation_workflow

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

- **異なるLLMプロバイダー**: 現在はGoogle Geminiモデルを使用していますが、OpenAIモデルやAnthropicモデルなど他のプロバイダーも使用可能です。
- **指示の詳細化**: `instruction`パラメータを詳細にすることでスライドの内容や方向性を調整できます

## 📂 プロジェクト構造

```
slide-generator-langchain/
│
├── src/                             # ソースコード
│   ├── application/                 # アプリケーション固有のコード
│   │   ├── graphs/                  # スライド生成のグラフコンポーネント
│   │   │   ├── __init__.py
│   │   │   ├── nodes.py            # スライド生成の処理ノード
│   │   │   └── states.py           # スライド生成の状態定義
│   │   ├── prompts/                 # スライド生成のプロンプト
│   │   │   ├── __init__.py
│   │   │   ├── extract_content_structure_prompt.py
│   │   │   ├── generate_detailed_slides_prompt.py
│   │   │   ├── generate_html_slides_prompt.py
│   │   │   ├── generate_slide_outline_prompt.py
│   │   │   └── process_image_prompt.py
│   │   ├── templates/               # スライドのHTMLテンプレート
│   │   │   ├── __init__.py
│   │   │   ├── default.html
│   │   │   └── modern.html
│   │   └── workflow.py              # メインワークフローの定義
│   │
│   └── core/                        # 再利用可能なコアコンポーネント
│       ├── graphs/                  # グラフ構造の基本要素
│       │   ├── __init__.py
│       │   ├── elements.py          # グラフノードの基本クラス
│       │   ├── networks.py          # ワークフロー構造の定義
│       │   └── states.py            # 状態管理の基本クラス
│       ├── llm/                     # 言語モデル連携
│       │   ├── __init__.py
│       │   ├── factory.py           # モデルファクトリー
│       │   ├── models.py            # 統一モデルインターフェース
│       │   ├── providers/           # 各プロバイダー実装
│       │   │   ├── __init__.py
│       │   │   ├── anthropic.py
│       │   │   ├── google.py
│       │   │   └── openai.py
│       │   └── utils.py             # ユーティリティ関数
│       ├── prompts/                 # プロンプト管理
│       │   ├── __init__.py
│       │   ├── examples/            # 例示用プロンプト
│       │   │   ├── __init__.py
│       │   │   ├── extract_content_structure_prompt.py
│       │   │   └── process_image_prompt.py
│       │   └── managers.py          # プロンプト管理クラス
│       └── templates/               # テンプレート管理
│           ├── __init__.py
│           ├── example.html
│           └── managers.py          # テンプレート管理クラス
│
├── examples/               # 使用例
├── docs/                   # ドキュメント
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

## 📖 詳細なドキュメント

詳細な使用方法とAPIリファレンスは、[docs](./docs)ディレクトリを参照してください。

---

**Note**: このプロジェクトは開発段階です。機能や実装が今後も拡張・変更される可能性があります。