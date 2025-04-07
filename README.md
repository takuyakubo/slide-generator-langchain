# 📊 Slide Generator

LangChainとLangGraphを使用してPDFやHTMLドキュメントから自動的にスライドプレゼンテーションを生成するツールです。

## 📋 概要

このプロジェクトは、PDFやHTML形式のテキスト文書（教科書、論文、ブログ記事など）を分析し、その内容に基づいて構造化されたHTML形式のスライドプレゼンテーションを自動生成します。LangChainのドキュメント処理機能とLangGraphのワークフロー管理機能を組み合わせて、効率的かつカスタマイズ可能なパイプラインを実現します。

## 🌟 主な機能

- PDF/HTMLドキュメントの読み込みと前処理
- 文書の構造と主要コンテンツの自動抽出
- スライドのアウトラインと詳細コンテンツの生成
- カスタマイズ可能なHTMLテンプレートを使用したスライド生成
- 数式、箇条書き、引用などの適切な書式設定
- Jupyter Notebookによる対話的な実行環境

## 🛠️ 前提条件

- Python 3.9+
- Jupyter Lab/Notebook
- OpenAI API キーまたはAnthropic API キー（LLMアクセス用）

## 📦 主要な依存関係

- `langchain`：ドキュメント処理および言語モデルとの統合用
- `langgraph`：ワークフロー構築および管理用
- `pypdf`：PDFファイル処理用
- `unstructured`：HTML/テキスト処理用
- `pydantic`：データモデリング用
- `openai` または `anthropic`：LLMサービスとの連携用

## 📝 ノートブック構成

このリポジトリには以下のJupyter Notebookが含まれる予定です：

1. `01_document_processing.ipynb` - ドキュメントの読み込みと前処理の基本
2. `02_content_extraction.ipynb` - 文書からの構造および主要コンテンツの抽出
3. `03_slide_generation.ipynb` - スライドアウトラインと詳細内容の生成
4. `04_html_conversion.ipynb` - スライドコンテンツのHTML形式への変換
5. `05_end_to_end_pipeline.ipynb` - 完全な自動化パイプラインの実装例

## 🚀 使用方法（予定）

### 基本的な使用手順

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

3. Jupyter Notebookの起動
   ```bash
   jupyter lab
   ```

4. ノートブックを開いて対話的に実行

### カスタマイズオプション

- カスタムHTMLテンプレートの使用
- スライドスタイルの選択（デフォルト、モダン、アカデミック）
- 異なるLLMプロバイダーの選択
- チャンクサイズと分割パラメータの調整

## 📂 プロジェクト構造

```
slide-generator-langchain/
│
├── notebooks/              # Jupyter Notebooks
├── templates/              # HTMLテンプレート
├── examples/               # 入出力例
├── utils/                  # ユーティリティスクリプト
├── requirements.txt        # 依存関係
├── .env.example            # 環境変数のサンプル
└── README.md               # このファイル
```

## 🔍 今後の改善点

- 画像抽出と処理の追加
- より洗練されたドキュメント構造解析
- スライドデザインのバリエーション拡充
- バッチ処理機能の追加
- WebUIの開発

## 🤝 コントリビューション

Issue提出やPull Requestは大歓迎です。大きな変更を加える前には、まずIssueを開いて変更内容について議論してください。

---

**Note**: このプロジェクトは開発初期段階です。機能や実装が変更される可能性があります。
