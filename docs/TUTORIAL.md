# Slide Generator チュートリアル

このチュートリアルでは、Slide Generatorを使って画像からスライドを生成する基本的な流れを説明します。

## ステップ1: 環境のセットアップ

まず、必要な環境をセットアップします。

```bash
# リポジトリのクローン
git clone https://github.com/takuyakubo/slide-generator-langchain.git
cd slide-generator-langchain

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .envファイルをエディタで開き、APIキーを設定
```

## ステップ2: サンプル画像の準備

スライドに変換したい画像を用意します。このチュートリアルでは、以下のようなフォルダ構造を想定します：

```
slide-generator-langchain/
└── examples/
    └── images/
        ├── slide1.png
        ├── slide2.png
        └── slide3.png
```

画像は順番に並べられており、スライドの順序を反映しているのが理想的です。

## ステップ3: 基本的なスライド生成

以下のPythonスクリプトを作成して実行します。名前は `my_first_slide.py` とします：

```python
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

# 環境変数の読み込み
load_dotenv()

# プロジェクトルートへのパスを追加
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.workflow import create_slide_generation_workflow

def main():
    # 画像パスの設定
    image_folder = Path("examples/images")
    image_paths = sorted([str(image_folder / f) for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
    
    # 指示の設定
    instruction = """
    これらの画像をもとに、技術解説用のスライドを作成してください。
    スライドのタイトルは「画像認識入門」としてください。
    """
    
    # ワークフローの作成とスライド生成
    app = create_slide_generation_workflow()
    result = app.invoke({
        "images": image_paths,
        "instruction": instruction
    })
    
    # 結果の保存
    output_path = "my_first_slide.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result["html_output"])
    
    print(f"スライドが生成されました: {output_path}")

if __name__ == "__main__":
    main()
```

このスクリプトを実行します：

```bash
python my_first_slide.py
```

実行が完了すると、`my_first_slide.html`というHTMLファイルが生成されます。このファイルをブラウザで開くと、生成されたスライドを閲覧できます。

## ステップ4: 指示のカスタマイズ

より良い結果を得るためには、指示を詳細にカスタマイズすることが重要です。以下に様々な指示の例を示します：

### 教育用スライド

```python
instruction = """
これらの画像をもとに、大学1年生向けのプログラミング入門講義用スライドを作成してください。
以下の点に注意してください：
1. 専門用語は最小限に抑え、初心者にもわかりやすい説明を心がける
2. 各概念には具体的な例を含める
3. スライドは視覚的に明快で、1枚あたりの情報量は少なめにする
4. 最後にまとめと次回の予告を含める
"""
```

### ビジネスプレゼンテーション

```python
instruction = """
これらの画像をもとに、役員会議向けのプロジェクト進捗報告スライドを作成してください。
以下の点に注意してください：
1. 簡潔で要点を押さえた内容にする
2. データは視覚的にわかりやすく表現する
3. 現状の課題と解決策を明確に示す
4. 次のステップとタイムラインを含める
5. 全体的に専門的かつ簡潔なトーンを維持する
"""
```

### 技術説明会

```python
instruction = """
これらの画像をもとに、エンジニア向けの新技術紹介スライドを作成してください。
以下の点に注意してください：
1. 技術的な詳細を正確に伝える
2. 実装例やコード例を含める
3. 既存技術との比較を示す
4. パフォーマンスデータや評価指標を視覚的に表現する
5. 実際の応用例と将来の展望を含める
"""
```

## ステップ5: 出力のカスタマイズ

生成されたHTMLをさらにカスタマイズする方法として、CSSの追加や基本的なJavaScriptの修正があります。以下に例を示します：

```python
def customize_html(html_content):
    # カスタムCSSの追加
    custom_css = """
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            background-color: #f5f5f5;
        }
        .slide {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            background-color: white;
        }
        .slide-title {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
        }
        .controls button {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        .controls button:hover {
            background-color: #2980b9;
        }
    </style>
    """
    
    # CSSをヘッドに追加
    html_content = html_content.replace('</head>', f'{custom_css}</head>')
    
    return html_content

# メイン関数内で使用
result = app.invoke({
    "images": image_paths,
    "instruction": instruction
})

html_output = customize_html(result["html_output"])

with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_output)
```

## ステップ6: 応用例 - ページ番号の追加

スライドにページ番号を追加するカスタマイズの例です：

```python
def add_page_numbers(html_content):
    # スライドの div 終了タグの前にページ番号表示用の div を追加
    page_number_div = """
    <div class="page-number" style="position: absolute; bottom: 10px; right: 20px; font-size: 14px; color: #666;"></div>
    """
    
    html_content = html_content.replace('</div>\n            \n            <div class="controls">', 
                                       f'{page_number_div}</div>\n            \n            <div class="controls">')
    
    # ページ番号を表示するJavaScriptコードを追加
    page_number_script = """
    // ページ番号の表示
    function updatePageNumber() {
        const pageNumbers = document.querySelectorAll('.page-number');
        pageNumbers.forEach((el, i) => {
            el.textContent = `${i+1} / ${slides.length}`;
        });
    }
    
    // 初期表示とスライド切り替え時にページ番号を更新
    updatePageNumber();
    document.getElementById('prev').addEventListener('click', updatePageNumber);
    document.getElementById('next').addEventListener('click', updatePageNumber);
    """
    
    # スクリプトの終了タグの前にコードを追加
    html_content = html_content.replace('</script>', f'{page_number_script}</script>')
    
    return html_content
```

## まとめ

このチュートリアルでは、Slide Generatorを使用して画像からスライドを生成する基本的な方法を学びました。

より高度な使用法については、以下のドキュメントを参照してください：
- [使用ガイド](USAGE.md) - 詳細な使用方法
- [APIリファレンス](API_REFERENCE.md) - API詳細

また、[examples](../examples)ディレクトリには、より多くの使用例が含まれています。
