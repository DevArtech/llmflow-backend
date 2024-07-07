from fastapi import APIRouter

from .contracts import llms, inputs, outputs, chat, helpers

router = APIRouter()
router.include_router(inputs.router, prefix="/inputs", tags=["Input Options"])
router.include_router(chat.router, prefix="/chat", tags=["Chat Options"])
router.include_router(llms.router, prefix="/llms", tags=["LLM Models"])
router.include_router(helpers.router, prefix="/helpers", tags=["Helper Functions"])
router.include_router(outputs.router, prefix="/outputs", tags=["Output Options"])
