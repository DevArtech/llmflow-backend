from fastapi import APIRouter

from .endpoints import llms, inputs, outputs

router = APIRouter()
router.include_router(llms.router, prefix="/llm-models", tags=["LLM Models"])
router.include_router(inputs.router, prefix="/input-options", tags=["Input Options"])
router.include_router(outputs.router, prefix="/output-options", tags=["Output Options"])