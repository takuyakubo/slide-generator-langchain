from .extract_content_structure_prompt import extract_content_structure_prompt
from .generate_detailed_slides_prompt import generate_detailed_slides_prompt
from .generate_html_slides_prompt import generate_html_slides_prompt
from .generate_slide_outline_prompt import generate_slide_outline_prompt
from .process_image_prompt import process_image_prompt

__all__ = [
    "process_image_prompt",
    "extract_content_structure_prompt",
    "generate_slide_outline_prompt",
    "generate_detailed_slides_prompt",
    "generate_html_slides_prompt",
]
