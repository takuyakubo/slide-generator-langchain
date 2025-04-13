from typing import Type

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import PrivateAttr


# モデルクラスを動的に生成する関数
def create_unified_model_class(base_class: Type):
    _unified_model_name: str = PrivateAttr(default="")

    class UnifiedModelClass(base_class):
        def __init__(self, model: str, *args, **kwargs):
            super().__init__(model=model, *args, **kwargs)
            self._unified_model_name = model

        @property
        def model(self) -> str:
            """どのモデルでも一貫してモデル名を返す"""
            return self._unified_model_name

    # クラス名を分かりやすくする
    UnifiedModelClass.__name__ = f"Unified{base_class.__name__}"
    return UnifiedModelClass


class ModelFactory:
    @staticmethod
    def create(provider: str, model_name: str, *args, **kwargs):
        """モデルプロバイダー名からUnifiedModelインスタンスを作成"""
        provider_map = {
            "openai": ChatOpenAI,
            "anthropic": ChatAnthropic,
            "google": ChatGoogleGenerativeAI,
        }

        if provider.lower() not in provider_map:
            raise ValueError(f"対応していないプロバイダーです: {provider}")

        base_class = provider_map[provider.lower()]
        unified_class = create_unified_model_class(base_class)
        return unified_class(model=model_name, *args, **kwargs)
