import traceback
import gradio as gr
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from version import __version__
from api.modules.modules import *
from api.api import model
from api.api import router as api_router
from middleware.logging_middleware import logger, LoggingMiddleware

DESC = """
LLMFlow is a no-code solution to quickly build and test your own language model pipelines. \\
All you need to do is drag and drop the components you need and connect them together! \\
Results are displayed in real-time and you can even chat with your model using the live rendering.
"""

API = "/api/v1"

app = FastAPI(title="LLMFLow", description=DESC, version=__version__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.add_middleware(LoggingMiddleware)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unexpected error occurred.", "detail": str(exc)},
    )


@app.get(
    "/",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).

    Returns:
    - HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


model.render_elements()

app = gr.mount_gradio_app(app, model.io, path="/gradio")
app.include_router(api_router, prefix=API)
