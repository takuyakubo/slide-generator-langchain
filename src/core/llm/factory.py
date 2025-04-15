from typing import Dict, Type

from core.llm.models import UnifiedModel
from core.llm.providers import get_provider, model_registory


class ModelFactory:
    """
    Factory class for creating language model instances.

    This class provides methods for creating model instances from different
    providers with a unified interface.
    """

    # Registry of provider-specific model implementations
    _registry: Dict[str, Type[UnifiedModel]] = model_registory

    @classmethod
    def create(cls, model_name: str, **kwargs) -> UnifiedModel:
        """
        Create a model instance for the specified model name.

        Args:
            model_name: Name of the model
            **kwargs: Additional arguments for the model

        Returns:
            Unified model instance

        Raises:
            ValueError: If the provider is not supported or not registered
        """
        provider = get_provider(model_name)
        if provider not in cls._registry:
            raise ValueError(
                f"Provider '{provider}' is not registered. "
                f"Available providers: {list(cls._registry.keys())}"
            )
        model_class = cls._registry[provider]
        return model_class(model_name, **kwargs)
