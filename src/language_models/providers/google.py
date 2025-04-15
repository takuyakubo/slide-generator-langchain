"""
Google Gemini model implementation.
"""

from langchain_google_genai import ChatGoogleGenerativeAI

from language_models.models import UnifiedModel

provider_name = "google"


class GoogleModel(ChatGoogleGenerativeAI, UnifiedModel):
    """
    Implementation of the unified model interface for Google Gemini models.
    """

    def __init__(self, model_name: str, **kwargs):
        """
        Initialize the Google model.

        Args:
            model_name: Google Gemini model name
            **kwargs: Additional arguments for the model
        """
        super(ChatGoogleGenerativeAI, self).__init__(model=model_name, **kwargs)
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
        """
        Invokes the Google model with the given prompt.
        
        Args:
            prompt: Formatted prompt messages
            **kwargs: Additional arguments for the model
            
        Returns:
            Model response as a string
        """
        response = self._client.invoke(prompt, **kwargs)
        return response.content
