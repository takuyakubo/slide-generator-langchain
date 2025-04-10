"""
画像からスライドを生成する例

このスクリプトは、複数の画像を入力として、それらをもとにスライドを生成します。
生成されたスライドはHTML形式で保存されます。
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv(override=True)

# プロジェクトルートへのパスを追加
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.workflow import create_slide_generation_workflow


def generate_slides_from_images(image_paths, instruction, output_path="generated_slides.html"):
    """
    画像からスライドを生成する関数
    
    Args:
        image_paths (list): 画像ファイルへのパスのリスト
        instruction (str): スライド生成のための指示
        output_path (str): 生成されるHTMLファイルの保存先パス
    
    Returns:
        str: 生成されたHTMLコード
    """
    try:
        # 画像ファイルの存在確認
        for img_path in image_paths:
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"画像ファイルが見つかりません: {img_path}")
        
        # ワークフローアプリケーションの作成
        app = create_slide_generation_workflow()
        
        # スライド生成の実行
        result = app.invoke({
            "images": image_paths,
            "instruction": instruction
        })
        
        # 生成されたHTMLの取得
        html_output = result["html_output"]
        
        # HTMLをファイルに保存
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_output)
        
        print(f"スライドが正常に生成されました: {output_path}")
        return html_output
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return None

if __name__ == "__main__":
    # 使用例
    image_paths = [
        # 画像ファイルのパスを指定（以下は例）
        "/path/to/your/image1.png",
        "/path/to/your/image2.png",
        "/path/to/your/image3.png"
    ]
    
    instruction = """
    これらの画像をもとに、勉強会用のスライドを作成してください。
    スライドは明確な構造を持ち、重要なポイントが強調されるようにしてください。
    """
    
    generate_slides_from_images(image_paths, instruction)
