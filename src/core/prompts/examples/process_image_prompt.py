from langchain_core.messages import HumanMessage
from llm.providers import ProviderType
from prompts.managers import PromptManager

process_image_prompt = PromptManager("process_image_prompt")
content = [
    HumanMessage(
        content=[
            {
                "type": "text",
                "text": "画像の内容を詳細に分析してください。主要な要素、テキスト、構造を抽出してください。",
            }
        ]
    )
]
process_image_prompt[ProviderType.GOOGLE.value] = content
process_image_prompt.append_attach_key("img_data")
