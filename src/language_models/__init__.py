from typing import Type

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from pydantic import PrivateAttr


class ModelFactory:
    @classmethod
    def create(cls, model_name: str, *args, **kwargs):
        """モデルプロバイダー名からUnifiedModelインスタンスを作成"""
        _, base_class = cls.model_name_to_provider_and_class(model_name)
        unified_class = cls.create_unified_model_class(base_class)
        return unified_class(model=model_name, *args, **kwargs)

    @staticmethod
    def model_name_to_provider_and_class(model_name: str):
        # モデル名から情報を抽出する関数。先々model名が同一でproviderが違うときはここにDSLを作成すること
        if model_name.startswith("claude-"):
            return "anthropic", ChatAnthropic
        elif model_name.startswith("gemini-"):
            return "google_api", ChatGoogleGenerativeAI
        elif model_name.startswith("gpt-"):
            return "openai", ChatOpenAI
        else:
            raise ValueError(f"対応していないモデル名です: {model_name}")

    @staticmethod
    def create_unified_model_class(base_class: Type):
        # モデルクラスを動的に生成する関数
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
