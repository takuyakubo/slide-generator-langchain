from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from workflow.base import SequentialWorkflow
from workflow.nodes import (
    ExtractContentStructure,
    GenerateDetailedSlides,
    GenerateHtmlSlides,
    GenerateSlideOutline,
    ProcessImages,
)
from workflow.states import SlideGenerationState


def create_slide_generation_workflow():
    """
    スライド生成ワークフローを作成する関数

    Returns:
        コンパイルされたLangGraphアプリケーション
    """
    # TBD make ModelManager/Factory
    """
    llm_5000 = ChatAnthropic(model="claude-3-7-sonnet-latest", max_tokens=5000)
    llm_1000 = ChatAnthropic(model="claude-3-7-sonnet-latest", max_tokens=1000)
    """
    llm_5000 = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro-preview-03-25", max_tokens=5000
    )
    llm_50000 = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro-preview-03-25", max_tokens=50000
    )
    """
    class ChatOpenAI_(ChatOpenAI):
        @property
        def model(self):
            return self.model_name
    llm_5000 = ChatOpenAI_(
        model="gpt-4o-mini", max_tokens=5000
    )
    llm_50000 = ChatOpenAI_(
        model="gpt-4o-mini", max_tokens=16384
    )
    """
    nodes = [
        ProcessImages(llm_5000),
        ExtractContentStructure(llm_5000),
        GenerateSlideOutline(llm_5000),
        GenerateDetailedSlides(llm_5000),
        GenerateHtmlSlides(llm_50000),
    ]
    wf = SequentialWorkflow(nodes, SlideGenerationState)
    return wf.get_app()
