from langfuse.callback import CallbackHandler

from config import LANGFUSE_HOST, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, USE_LANGFUSE
from language_models.factory import ModelFactory
from workflow.base import SequentialWorkflow
from workflow.nodes import (
    ExtractContentStructure,
    GenerateDetailedSlides,
    GenerateHtmlSlides,
    GenerateSlideOutline,
    ProcessImages,
)
from workflow.states import SlideGenerationState

langfuse_handler = CallbackHandler(
    public_key=LANGFUSE_PUBLIC_KEY,
    secret_key=LANGFUSE_SECRET_KEY,
    host=LANGFUSE_HOST,
)


def create_slide_generation_workflow():
    """
    スライド生成ワークフローを作成する関数

    Returns:
        コンパイルされたLangGraphアプリケーション
    """
    # llm_small = ModelFactory.create(model_name="gpt-4o-mini", max_tokens=5000)
    # llm_large = ModelFactory.create(model_name="gpt-4o-mini", max_tokens=16384)
    # llm_small = ModelFactory.create(model_name="claude-3-7-sonnet-latest", max_tokens=5000)
    # llm_large = ModelFactory.create(model_name="claude-3-7-sonnet-latest", max_tokens=10000)
    llm_small = ModelFactory.create(
        model_name="gemini-2.5-pro-preview-03-25", max_tokens=5000
    )
    llm_large = ModelFactory.create(
        model_name="gemini-2.5-pro-preview-03-25", max_tokens=50000
    )
    nodes = [
        ProcessImages(llm_small),
        ExtractContentStructure(llm_small),
        GenerateSlideOutline(llm_small),
        GenerateDetailedSlides(llm_small),
        GenerateHtmlSlides(llm_large),
    ]
    wf = SequentialWorkflow(nodes, SlideGenerationState)
    app = wf.get_app()
    if USE_LANGFUSE:
        app = app.with_config({"callbacks": [langfuse_handler]})
    return app
