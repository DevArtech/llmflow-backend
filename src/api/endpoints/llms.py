from fastapi import APIRouter, status
from ..modules.modules import AvailableLLMs, TextItem, DropdownItem, Node, NumberItem, TextDisplay, HandleElement

router = APIRouter()

@router.get("/", summary="Get all available large language models", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK, response_model=AvailableLLMs)
async def get_models():
    return AvailableLLMs(models=["OpenAI", "Gemini", "Ollama"])

@router.get("/openai", summary="Get the OpenAI model node", response_description="Return the OpenAI model node", status_code=status.HTTP_200_OK)
async def get_openai():
    node = Node(
        icon="OpenAI",
        name="OpenAI Model",
        items=[
            HandleElement(label="Cache", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="API Key", placeholder="sk-..."),
            DropdownItem(label="Model", options=["gpt-3.5-turbo-0125", "gpt-4o", "gpt-4-turbo", "gpt-4"]),
            NumberItem(label="Temperature", min=0.0, max=1.0, step=0.01, initial=0.7),
            TextDisplay(text="Output"),
            HandleElement(label="OpenAI", position="right", type="source", style={"bottom": 12, "top": "auto"}),
        ]
    )

    return node.to_dict()

@router.get("/gemini", summary="Get the Gemini model node", response_description="Return the Gemini model node", status_code=status.HTTP_200_OK)
async def get_gemini():
    node = Node(
        icon="Gemini",
        name="Gemini Model",
        items=[
            HandleElement(label="Cache", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="API Key", placeholder="sk-..."),
            DropdownItem(label="Model", options=["gemini-1.5-flash", "gemini-1.5-pro"]),
            TextDisplay(text="Output"),
            HandleElement(label="Gemini", position="right", type="source", style={"bottom": 12, "top": "auto"}),
        ]
    )

    return node.to_dict()

@router.get("/ollama", summary="Get the Ollama model node", response_description="Return the Ollama model node", status_code=status.HTTP_200_OK)
async def get_ollama():
    node = Node(
        icon="Ollama",
        name="Ollama Model",
        items=[
            HandleElement(label="Cache", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="Base URL", placeholder="http://localhost:1234", type="url"),
            DropdownItem(label="Model", options=["llama3", "llama2"]),
            NumberItem(label="Temperature", min=0.0, max=1.0, step=0.01, initial=0.7),
            TextDisplay(text="Output"),
            HandleElement(label="Ollama", position="right", type="source", style={"bottom": 12, "top": "auto"}),
        ]
    )

    return node.to_dict()