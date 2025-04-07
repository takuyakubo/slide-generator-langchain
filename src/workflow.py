from langchain_anthropic import ChatAnthropic
from workflow_nodes import ProcessImages, ExtractContentStructure, GenerateSlideOutline, GenerateDetailedSlides, GenerateHtmlSlides
from workflow_states import SlideGenerationState
from workflow_base import SequentialWorkflow

def create_slide_generation_workflow():
    llm_5000 = ChatAnthropic(model="claude-3-7-sonnet-latest", max_tokens=5000)
    llm_1000 = ChatAnthropic(model="claude-3-7-sonnet-latest", max_tokens=1000)
    nodes = [
        ProcessImages(llm_1000),
        ExtractContentStructure(llm_1000),
        GenerateSlideOutline(llm_1000),
        GenerateDetailedSlides(llm_1000),
        GenerateHtmlSlides(llm_5000)]
    wf = SequentialWorkflow(nodes, SlideGenerationState)
    return wf.get_app()