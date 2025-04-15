"""
OpenAI model implementation.
"""

from langchain_openai import ChatOpenAI

from core.llm.models import UnifiedModel
from core.llm.utils import image_path_to_image_data

provider_name = "openai"


class OpenAIModel(ChatOpenAI, UnifiedModel):
    """
    Implementation of the unified model interface for OpenAI models.
    """

    def __init__(self, model_name: str, **kwargs):
        """
        Initialize the OpenAI model.

        Args:
            model_name: OpenAI model name
            **kwargs: Additional arguments for the model
        """
        super(ChatOpenAI, self).__init__(model=model_name, **kwargs)
        self._model_name = model_name

    @property
    def model_name(self) -> str:
        """
        Returns the name of the underlying model.
        """
        return self._model_name

    @property
    def provider_name(self) -> str:
        """
        Returns the name of the model provider.
        """
        return provider_name

    @staticmethod
    def get_image_object(image_path) -> dict:
        mime_type, image_data = image_path_to_image_data(image_path)
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{image_data}"},
        }
