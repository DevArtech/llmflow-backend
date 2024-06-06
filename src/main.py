import json
from fastapi import FastAPI, status
from pydantic import BaseModel
import uvicorn
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"

@app.get("/health", tags=["healthcheck"], summary="Perform a Health Check", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK, response_model=HealthCheck)
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

@app.get("/api/v2/get-node", tags=["node"], summary="Get the Node Name", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK)
def get_node() -> Dict[str, str]:
    """
    ## Get an Example Node
    Endpoint to get an example node. This endpoint is primarily used to demonstrate
    how to return a JSON response from an API endpoint.
    Returns:
        Dict[str, str]: Returns a JSON response with the node info
    """
    node = json.dumps({
            "name": "API Test Node",
            "items": {
                "text": {
                  "label": "Test",
                  "placeholder": "Testing Node",
                },
                "file": {
                  "label": "File",
                },
                "bezierCurve": {
                  "label": "Bezier Curve",
                  "initialHandles": [
                    { "x": 0, "y": 0 },
                    { "x": 0, "y": 200 },
                    { "x": 300, "y": 0 },
                    { "x": 300, "y": 200 },
                  ],
                  "maxX": 300,
                  "maxY": 200,
                },
              }
            }
          )
    return { "result" : node }

