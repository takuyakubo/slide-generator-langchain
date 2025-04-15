from enum import Enum

from core.llm.providers.anthropic import AnthropicModel
from core.llm.providers.anthropic import provider_name as apn
from core.llm.providers.google import GoogleModel
from core.llm.providers.google import provider_name as gpn
from core.llm.providers.openai import OpenAIModel
from core.llm.providers.openai import provider_name as opn

"""
Provider-specific implementations of the unified model interface.
"""


class ProviderType(Enum):
    """
    Enumeration of supported LLM providers.
    """

    ANTHROPIC = apn
    OPENAI = opn
    GOOGLE = gpn


model_registory = {
    ProviderType.ANTHROPIC.value: AnthropicModel,
    ProviderType.OPENAI.value: OpenAIModel,
    ProviderType.GOOGLE.value: GoogleModel,
}


def get_provider(model_name: str) -> str:
    """
    Determine the provider from the model name.

    Args:
        model_name: Name of the model

    Returns:
        Provider name

    Raises:
        ValueError: If the provider cannot be determined
    """
    if model_name.startswith("claude-"):
        return ProviderType.ANTHROPIC.value
    elif model_name.startswith("gemini-"):
        return ProviderType.GOOGLE.value
    elif model_name.startswith("gpt-"):
        return ProviderType.OPENAI.value
    else:
        raise ValueError(f"Cannot determine provider for model: {model_name}")
