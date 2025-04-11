import base64
import os

import pytest
from PIL import Image

from src.utils import image_to_image_data_str


def test_image_to_image_data_str_with_pil_image():
    # テスト用のPILイメージを作成
    img = Image.new("RGB", (100, 100), color="red")

    # 関数を実行
    result = image_to_image_data_str(img)

    # 結果がbase64エンコードされた文字列であることを確認
    assert isinstance(result, str)
    assert len(result) > 0

    # base64デコードして元の画像データが正しくエンコードされていることを確認
    decoded = base64.b64decode(result)
    assert len(decoded) > 0


def test_image_to_image_data_str_with_file_path(tmp_path):
    # テスト用の画像ファイルを作成
    img = Image.new("RGB", (100, 100), color="blue")
    img_path = os.path.join(tmp_path, "test.png")
    img.save(img_path)

    # 関数を実行
    result = image_to_image_data_str(img_path)

    # 結果がbase64エンコードされた文字列であることを確認
    assert isinstance(result, str)
    assert len(result) > 0

    # base64デコードして元の画像データが正しくエンコードされていることを確認
    decoded = base64.b64decode(result)
    assert len(decoded) > 0


def test_image_to_image_data_str_with_invalid_input():
    # サポートされていない入力タイプで例外が発生することを確認
    with pytest.raises(Exception) as exc_info:
        image_to_image_data_str(123)  # 数値はサポートされていない

    assert "サポートされていない画像形式です" in str(exc_info.value)
