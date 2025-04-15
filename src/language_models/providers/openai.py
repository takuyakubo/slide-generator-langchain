"""
OpenAI model implementation.
"""

from langchain_openai import ChatOpenAI

from language_models.models import UnifiedModel

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
