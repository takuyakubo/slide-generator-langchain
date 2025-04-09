# Slide Generator 使用ガイド

このドキュメントでは、Slide Generatorの詳細な使い方を説明します。

## 1. セットアップ

### 環境のセットアップ

1. リポジトリのクローン:
   ```bash
   git clone https://github.com/takuyakubo/slide-generator-langchain.git
   cd slide-generator-langchain
   ```

2. 仮想環境の作成と依存関係のインストール:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windowsの場合: venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. 環境変数の設定:
   `.env.example`ファイルを`.env`としてコピーし、必要なAPI情報を追加してください。
   ```bash
   cp .env.example .env
   # .envファイルを編集してAPIキーを設定（現在はGoogle Gemini API用に設定してください）
   ```

## 2. 基本的な使い方

### 画像からスライドを生成する

最もシンプルな使用例は、画像ファイルからスライドを生成することです。

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
with open("slide_output.html", "w", encoding="utf-8") as f:
    f.write(result["html_output"])
```

## 3. 入力パラメータの詳細

### 画像入力

画像はファイルパスのリストとして提供します：

```python
"images": [
    "/path/to/your/image1.png", 
    "/path/to/your/image2.png"
]
```

サポートしている画像形式：
- PNG
- JPEG/JPG
- 他の一般的な画像フォーマット

### 指示 (instruction)

指示は、スライド生成に関する具体的なリクエストです。より詳細で具体的な指示を提供することで、より的確なスライドが生成されます。

**指示の例:**

```
"これらの画像をもとに、初心者向けのPython入門講座のスライドを作成してください。各概念を簡潔に説明し、実例を含めてください。"
```

**より効果的な指示のコツ:**

- 対象読者を明確にする（例：初心者向け、エンジニア向けなど）
- スライドの目的を明示する（例：講義用、プレゼンテーション用）
- トーンやスタイルの要望を含める（例：カジュアル、フォーマル）
- 具体的な構成の要望があれば添える

## 4. 処理フローの詳細

Slide Generatorは次の5つのステップでスライドを生成します：

1. **画像処理（ProcessImages）**: 
   画像を分析し、内容を抽出します。画像に含まれるテキスト、図表、視覚的要素を認識します。

2. **構造抽出（ExtractContentStructure）**: 
   画像分析と指示を組み合わせて、スライドの基本構造を特定します。タイトル、サブタイトル、主要ポイント、結論などを決定します。

3. **アウトライン生成（GenerateSlideOutline）**: 
   スライドごとのアウトラインを作成します。各スライドのタイトル、内容の概要、必要な視覚的要素を計画します。

4. **詳細化（GenerateDetailedSlides）**: 
   各スライドの詳細な内容を生成します。完全な文章、段落構造、箇条書きなどを含む具体的な内容を作成します。

5. **HTML変換（GenerateHtmlSlides）**: 
   生成したスライド内容をHTMLフォーマットに変換します。スタイル設定、レイアウト、ナビゲーション機能を含むインタラクティブなスライドを生成します。

## 5. 出力形式

生成されるスライドはHTML形式で出力されます。出力には以下の特徴があります：

- レスポンシブデザイン
- スライド間のナビゲーション機能（前へ/次へボタン）
- 整形されたテキストとレイアウト
- モダンなスタイル設定

HTMLファイルは任意のウェブブラウザで開いて閲覧できます。

## 6. カスタマイズ

### 異なる言語モデルの使用

現在の実装ではGoogle Gemini Pro Previewモデルをデフォルトで使用しています。実装を変更して、他のLLMプロバイダーを使用することも可能です。

```python
from langchain_openai import ChatOpenAI
from src.workflow_nodes import ProcessImages, ExtractContentStructure, GenerateSlideOutline, GenerateDetailedSlides, GenerateHtmlSlides
from src.workflow_states import SlideGenerationState
from src.workflow_base import SequentialWorkflow

def create_custom_workflow():
    # OpenAIモデルを使用する例
    llm = ChatOpenAI(model="gpt-4", temperature=0.7)
    nodes = [
        ProcessImages(llm),
        ExtractContentStructure(llm),
        GenerateSlideOutline(llm),
        GenerateDetailedSlides(llm),
        GenerateHtmlSlides(llm)]
    wf = SequentialWorkflow(nodes, SlideGenerationState)
    return wf.get_app()
```

**注意**: `workflow.py`ファイル内の実装を変更する場合は、必要に応じて適切なAPIキーを設定してください。

## 7. エラー処理

一般的なエラーとその解決方法：

1. **API認証エラー**:
   - `.env`ファイルで正しいAPIキーが設定されているか確認してください
   - APIキーの有効期限が切れていないか確認してください
   - **現在はGoogle Gemini APIキーが必要です**

2. **画像読み込みエラー**:
   - ファイルパスが正しいか確認してください
   - サポートされている画像形式か確認してください

3. **メモリエラー**:
   - 大量の画像を扱う場合、メモリ制限に達する可能性があります
   - 画像数を減らすか、より低解像度の画像を使用してください

## 8. 高度な使用例

### 複数指示の組み合わせ

複数の指示を組み合わせて、より具体的なスライドを生成することができます。

```python
instruction = """
次の条件を満たすスライドを作成してください：
1. 大学生向けの機械学習入門講義用
2. 各スライドに簡潔な説明と具体例を含める
3. 数式は最小限に抑え、直感的な説明を心がける
4. 配色は青と白を基調とする
5. 最後に練習問題を3問含める
"""
```

### 結果の後処理

生成されたHTMLを後処理して、さらにカスタマイズすることができます。

```python
import re

# スライド生成
result = app.invoke({
    "images": image_paths,
    "instruction": instruction
})

html_output = result["html_output"]

# HTMLの後処理（例：特定のスタイルを追加）
html_output = html_output.replace(
    "</head>",
    "<link rel=\"stylesheet\" href=\"custom_style.css\"></head>"
)

# 生成されたHTMLを保存
with open("enhanced_slides.html", "w", encoding="utf-8") as f:
    f.write(html_output)
```

## 9. トラブルシューティング

- **問題**: スライドが生成されない、または内容が不完全
  **解決策**: 指示をより具体的にし、画像解像度が十分であることを確認

- **問題**: 画像内のテキストが正確に認識されない
  **解決策**: より高品質の画像を使用し、テキストが明確に読み取れることを確認

- **問題**: デザインが期待通りでない
  **解決策**: 生成後にCSSを編集して調整する

## 10. 今後の開発予定

現在、以下の機能の実装を計画しています：

- **ドキュメント処理機能**: PDF、HTMLなどの文書からのスライド生成機能
- **テンプレート選択機能**: 複数のHTMLテンプレートから選択できる機能
- **WebUI**: ブラウザからスライド生成を操作できるインターフェース

## 11. APIリファレンス

### create_slide_generation_workflow()

ワークフローアプリケーションを作成します。

**戻り値**:
- コンパイルされたLangGraphアプリケーション

### app.invoke(input_dict)

スライド生成処理を実行します。

**パラメータ**:
- `input_dict`: 入力パラメータの辞書
  - `images`: 画像パスのリスト
  - `instruction`: スライド生成の指示

**戻り値**:
- 結果を含む辞書
  - `html_output`: 生成されたHTMLスライド
  - その他の中間結果（画像分析、構造、アウトラインなど）