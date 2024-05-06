"""Original health endpoint template by Jarmos-san at: https://gist.github.com/Jarmos-san/0b655a3f75b698833188922b714562e5"""
"""Entrypoint to invoke the FastAPI application service with."""

from fastapi import FastAPI, status
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"

@app.get("/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,)
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


def main() -> None:
    """Entrypoint to invoke when this module is invoked on the local/remote server."""
    uvicorn.run("app:app", host="localhost")


if __name__ == "__main__":
    main()