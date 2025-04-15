import logging
from copy import deepcopy
from string import Formatter
from typing import Self

from langchain_core.messages import HumanMessage
from langchain_core.messages.base import BaseMessage
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)


def extract_variables_from(format_string):
    formatter = Formatter()
    variables = []
    for _, field_name, _, _ in formatter.parse(format_string):
        if field_name is not None:
            variables.append(field_name)
    return variables


def extract_vars(target, kws):
    if isinstance(target, list):
        for v in target:
            extract_vars(v, kws)
    elif isinstance(target, dict):
        for k in target:
            extract_vars(target[k], kws)
    elif isinstance(target, BaseMessage):
        extract_vars(target.content, kws)
    elif isinstance(target, str):
        kws += extract_variables_from(target)
    return kws


def assign_vars(target, kws):
    if isinstance(target, list):
        return [assign_vars(v, kws) for v in target]
    elif isinstance(target, dict):
        return {k: assign_vars(v, kws) for k, v in target.items()}
    elif isinstance(target, BaseMessage):
        return type(target)(assign_vars(target.content, kws))
    elif isinstance(target, str):
        return target.format(**kws)
    return target


class PromptManager:
    def __init__(self, prompt_name, description="", use_default=True) -> None:
        self.prompt_name = prompt_name
        self.prompt_description = description
        self.prompt_contents = dict()
        self.variables = []
        self.default_key = None
        self.get_item_logic = lambda x: x
        self.use_default = use_default
        self.attach_prefix = (
            "_attach_"  # DSLで_attach_　とついたkeyには添付で対応する。
        )

    def __setitem__(self, key, value) -> None:
        """
        特定のモデルキーに対してプロンプトを設定する
        """
        variables = extract_vars(value, [])
        if self.default_key is None:
            self.default_key = key
            self.variables = variables
        else:
            if set(self.variables) != set(variables):
                raise Exception(
                    "新しく設定するテンプレートは元のテンプレートと同一のformat変数を持たなくてはいけません。"
                )
        self.prompt_contents[key] = value

    def __getitem__(self, key: str) -> Self:
        key_ = self.get_item_logic(key)
        if key_ not in self.prompt_contents:
            if self.use_default:
                logger.warning(
                    f"{self.prompt_name}に対するkeyで想定外のものが呼び出されました。expected in: {list(self.prompt_contents.keys())}, actual: {key} -> {key_}"
                )
                return self
            else:
                raise Exception(
                    f"{self.prompt_name}に対するkeyは次のうちいずれかにして下さい: {list(self.prompt_contents.keys())}"
                )
        self.default_key = key_
        return self

    def __call__(self, kwargs):
        kws = kwargs.keys()
        if not (set(self.variables) <= set(kws)):
            raise Exception(
                f"{self.prompt_name}の呼び出しは、あらかじめ決められた引数が必要です。expected: {self.variables}, actual: {kws}"
            )
        prompt_content = deepcopy(self.prompt_contents[self.default_key])
        prompt_content = assign_vars(prompt_content, kwargs)
        attached_contents = []
        for k in kws:
            if k.startswith(self.attach_prefix):
                attached_contents = self.attach(kwargs[k], attached_contents)
        if attached_contents:
            prompt_content += [HumanMessage(content=attached_contents)]
        return ChatPromptTemplate(prompt_content)

    @staticmethod
    def attach(image_info, content_list):
        if isinstance(image_info, list):
            content_list += image_info
        elif isinstance(image_info, dict):
            content_list += [image_info]
        else:
            raise ValueError("添付できるタイプはlistかdictのみです。")
        return content_list

    def append_attach_key(self, key: str):
        self.variables += [self.attach_prefix + key]
