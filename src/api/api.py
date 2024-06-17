from fastapi import APIRouter

from .endpoints import llms, inputs, outputs

router = APIRouter()
router.include_router(llms.router, prefix="/llms", tags=["LLM Models"])
router.include_router(inputs.router, prefix="/inputs", tags=["Input Options"])
router.include_router(outputs.router, prefix="/outputs", tags=["Output Options"])