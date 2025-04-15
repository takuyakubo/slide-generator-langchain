import base64
import io
import mimetypes

from PIL import Image


def image_to_image_data_str(image):
    # 画像をbase64エンコード
    if isinstance(image, str):  # 画像がパスとして提供された場合
        with open(image, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    elif isinstance(image, Image.Image):  # PILイメージの場合
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    else:
        raise Exception(f"サポートされていない画像形式です (画像 {image})")


def image_path_to_image_data(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    image_data = image_to_image_data_str(image_path)
    return mime_type, image_data
