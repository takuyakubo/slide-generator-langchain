from langchain_core.messages import HumanMessage

from language_models.providers import ProviderType
from prompts.managers import PromptManager

process_image_prompt = PromptManager("process_image_prompt")
direction = {
    "type": "text",
    "text": "画像の内容を詳細に分析してください。主要な要素、テキスト、構造を抽出してください。",
}
img = {"type": "image_url", "image_url": {"url": "data:image/png;base64,{img_data}"}}
img_ = {
    "type": "image",
    "source": {"type": "base64", "media_type": "image/png", "data": "{img_data}"},
}
content = [HumanMessage(content=[direction, img])]
content_ = [HumanMessage(content=[direction, img_])]
process_image_prompt[ProviderType.GOOGLE.value] = content
process_image_prompt[ProviderType.OPENAI.value] = content
process_image_prompt[ProviderType.ANTHROPIC.value] = content_
