# API リファレンス

このドキュメントでは、Slide Generator APIの詳細なリファレンスを提供します。

## ワークフロー構成

### `create_slide_generation_workflow()`

スライド生成のワークフローを作成して返します。

**場所**: `src/workflow.py`

**戻り値**:
- コンパイルされたLangGraphアプリケーション

**使用例**:
```python
from src.workflow import create_slide_generation_workflow

app = create_slide_generation_workflow()
result = app.invoke(input_data)
```

## ワークフローノード

各ノードはスライド生成パイプラインの一部の処理を担当します。

### `ProcessImages`

画像を処理して内容を抽出します。

**場所**: `src/workflow_nodes.py`

**パラメータ**:
- `llm`: 使用する言語モデル

**主要メソッド**:
- `proc(state)`: 画像処理を実行し、分析結果を返します

**入力状態**:
- `state.images`: 処理する画像のリスト（パスまたはPILイメージオブジェクト）

**出力状態**:
- `state.image_content`: 画像分析結果のリスト

### `ExtractContentStructure`

画像分析と指示からスライドの構造を抽出します。

**場所**: `src/workflow_nodes.py`

**パラメータ**:
- `llm`: 使用する言語モデル

**主要メソッド**:
- `proc(state)`: 構造抽出処理を実行し、更新された状態を返します

**入力状態**:
- `state.instruction`: ユーザーの指示
- `state.image_content`: 画像分析結果

**出力状態**:
- `state.content_structure`: 抽出された構造情報

### `GenerateSlideOutline`

構造からスライドのアウトラインを生成します。

**場所**: `src/workflow_nodes.py`

**パラメータ**:
- `llm`: 使用する言語モデル

**主要メソッド**:
- `proc(state)`: アウトライン生成を実行し、更新された状態を返します

**入力状態**:
- `state.content_structure`: 抽出された構造情報

**出力状態**:
- `state.slide_outline`: 生成されたスライドアウトライン

### `GenerateDetailedSlides`

アウトラインから詳細なスライド内容を生成します。

**場所**: `src/workflow_nodes.py`

**パラメータ**:
- `llm`: 使用する言語モデル

**主要メソッド**:
- `proc(state)`: 詳細スライド生成を実行し、更新された状態を返します

**入力状態**:
- `state.slide_outline`: スライドのアウトライン

**出力状態**:
- `state.slide_presentation`: 詳細なスライドプレゼンテーション（通常はJSON形式）

### `GenerateHtmlSlides`

詳細なスライド内容からHTMLスライドを生成します。

**場所**: `src/workflow_nodes.py`

**パラメータ**:
- `llm`: 使用する言語モデル

**主要メソッド**:
- `proc(state)`: HTML生成を実行し、更新された状態を返します

**入力状態**:
- `state.slide_presentation`: 詳細なスライドプレゼンテーション

**出力状態**:
- `state.html_output`: 最終的なHTML出力

## 状態定義

### `SlideGenerationState`

スライド生成プロセス全体の状態を表すクラスです。

**場所**: `src/workflow_states.py`

**属性**:
- `images`: 画像のリスト（List[Any]）
- `instruction`: ユーザーからの指示（str）
- `image_content`: 画像分析結果（List[Dict[str, Any]]）
- `content_structure`: 構造化されたコンテンツ（str）
- `slide_outline`: スライドのアウトライン（str）
- `slide_presentation`: 詳細なスライドプレゼンテーション（str）
- `html_output`: 最終的なHTML出力（str）
- `error`: エラーメッセージ（str、NodeStateから継承）

## ベースクラス

### `NodeState`

すべての状態クラスの基底クラスです。

**場所**: `src/workflow_base.py`

**属性**:
- `error`: エラーメッセージ（存在する場合）

**メソッド**:
- `emit_error(error_str)`: エラーを設定した新しい状態を返します

### `LangGraphNode`

ワークフローのノードの基底クラスです。

**場所**: `src/workflow_base.py`

**属性**:
- `name`: ノードの名前
- `llm`: 使用する言語モデル

**メソッド**:
- `action(state)`: 実際の処理を実行するラッパーメソッド
- `proc(state)`: サブクラスでオーバーライドする処理メソッド
- `generate_node()`: ノード名と実行関数のタプルを返します
- `node_name()`: 正規化されたノード名を返します

### `LangGraphConditionalEdge`

条件付きエッジを表すクラスです。

**場所**: `src/workflow_base.py`

**メソッド**:
- `check_error(state)`: エラーがあるかどうかを確認します
- `args_conditional_edge()`: 条件付きエッジの引数を返します

### `SequentialWorkflow`

シーケンシャルなワークフローを構築するクラスです。

**場所**: `src/workflow_base.py`

**メソッド**:
- `setup(nodes)`: ワークフローのノードをセットアップします
- `get_app()`: コンパイルされたアプリケーションを返します

## 入力パラメータ

アプリケーションの `invoke()` メソッド呼び出しに使用できる入力パラメータ：

```python
input_data = {
    "images": [
        "/path/to/image1.png",
        "/path/to/image2.png"
    ],
    "instruction": "これらの画像をもとに、技術解説用のスライドを作成してください。"
}

result = app.invoke(input_data)
```

### images

画像のリスト。各画像は以下のいずれかの形式で指定できます：
- 文字列としてのファイルパス
- PILイメージオブジェクト

### instruction

スライド生成に関するユーザーの指示を含む文字列。明確で詳細な指示を提供することで、より良い結果が得られます。

## 出力パラメータ

`invoke()` メソッドの戻り値は、以下のキーを含む辞書です：

```python
result = {
    "images": [...],  # 入力画像
    "instruction": "...",  # 入力指示
    "image_content": [...],  # 画像分析結果
    "content_structure": "...",  # 抽出された構造
    "slide_outline": "...",  # スライドアウトライン
    "slide_presentation": "...",  # 詳細スライド内容
    "html_output": "...",  # 最終HTML出力
    "error": ""  # エラーがあれば表示
}
```

通常、最終結果である `html_output` のみを使用します。
