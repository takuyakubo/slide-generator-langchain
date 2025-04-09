from langchain_core.messages import HumanMessage
from prompts.managers import PromptManager
from prompts.key_logics import model_key_logic

process_image_prompt = PromptManager("process_image_prompt")
direction = {"type": "text", "text": "画像の内容を詳細に分析してください。主要な要素、テキスト、構造を抽出してください。"}
img = {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,{img_data}"}}
img_ = {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "{img_data}"}}
content = [HumanMessage(content=[direction, img])]
content_ = [HumanMessage(content=[direction, img_])]
process_image_prompt['gemini'] = content
process_image_prompt['claude'] = content_
process_image_prompt.get_item_logic = model_key_logic