import gradio as gr
from typing import Dict
from api.modules.modules import *
from fastapi import FastAPI, status
from api.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

io = gr.Blocks()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", summary="Perform a Health Check", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK, response_model=HealthCheck)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")

@app.get("/api/v1/integrations", summary="Get all available integrations", response_description="Return a list of all available integrations", status_code=status.HTTP_200_OK, response_model=AvailableIntegrations)
def get_integrations() -> AvailableIntegrations:
    """
    ## Get all available integrations
    Endpoint to get all available integrations that can be used in the LLMFlow.
    Returns:
        AvailableIntegrations: Returns a JSON response with all available integrations
    """
    return AvailableIntegrations(integrations=["Inputs", "LLMs", "Outputs"])

with io:
    gr.Markdown(
        """
        # Welcome to LLMFlow!
        Add some input and output nodes to see the magic happen!
        """
    )

app = gr.mount_gradio_app(app, io, path="/gradio")
app.include_router(api_router, prefix="/api/v1")
