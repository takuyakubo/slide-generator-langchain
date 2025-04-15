"""
Anthropic Claude model implementation.
"""

from langchain_anthropic import ChatAnthropic

from language_models.models import UnifiedModel

provider_name = "anthropic"


class AnthropicModel(ChatAnthropic, UnifiedModel):
    """
    Implementation of the unified model interface for Anthropic Claude models.
    """

    def __init__(self, model_name: str, **kwargs):
        """
        Initialize the Anthropic model.

        Args:
            model_name: Claude model name
            **kwargs: Additional arguments for the model
        """
        super(ChatAnthropic, self).__init__(model=model_name, **kwargs)
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
