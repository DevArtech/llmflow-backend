from fastapi import APIRouter, status
from ..modules.modules import (
    AvailableOptions,
    TextItem,
    DropdownItem,
    Node,
    SliderItem,
    TextDisplay,
    HandleElement,
    TextAreaItem,
    NodeContract,
)

router = APIRouter()


@router.get(
    "/",
    summary="Get all available large language models",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=AvailableOptions,
)
async def get_models():
    return AvailableOptions(
        options=[
            {"name": "OpenAI", "detail": "OpenAI LLM"},
            {"name": "Gemini", "detail": "Gemini LLM"},
            {"name": "Ollama", "detail": "Ollama LLM"},
        ]
    )


@router.get(
    "/openai",
    summary="Get the OpenAI model node",
    response_description="Return the OpenAI model node",
    status_code=status.HTTP_200_OK,
    response_model=NodeContract,
)
async def get_openai():
    node = Node(
        icon="OpenAI",
        name="OpenAI LLM",
        items=[
            HandleElement(label="Cache", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(
                label="API Key",
                placeholder="sk-...",
                type="password",
                required=True,
                hasHandle=True,
                handleStyle={"top": 104},
            ),
            DropdownItem(
                label="Model",
                options=["gpt-3.5-turbo-0125", "gpt-4o", "gpt-4-turbo", "gpt-4"],
                hasHandle=True,
                handleStyle={"top": 134},
            ),
            SliderItem(
                label="Temperature",
                min=0.0,
                max=2.0,
                step=0.01,
                initial=0.7,
                hasHandle=True,
                handleStyle={"top": 174},
            ),
            TextAreaItem(
                label="System Message", hasHandle=True, handleStyle={"top": 211}
            ),
            TextDisplay(text="Output"),
            HandleElement(
                label="OpenAI",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node.json()


@router.get(
    "/gemini",
    summary="Get the Gemini model node",
    response_description="Return the Gemini model node",
    status_code=status.HTTP_200_OK,
    response_model=NodeContract,
)
async def get_gemini():
    node = Node(
        icon="Gemini",
        name="Gemini LLM",
        items=[
            HandleElement(label="Cache", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(
                label="API Key",
                placeholder="sk-...",
                type="password",
                hasHandle=True,
                handleStyle={"top": 104},
            ),
            DropdownItem(
                label="Model",
                options=["gemini-1.5-flash", "gemini-1.5-pro"],
                hasHandle=True,
                handleStyle={"top": 134},
            ),
            TextDisplay(text="Output"),
            HandleElement(
                label="Gemini",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node.json()


@router.get(
    "/ollama",
    summary="Get the Ollama model node",
    response_description="Return the Ollama model node",
    status_code=status.HTTP_200_OK,
    response_model=NodeContract,
)
async def get_ollama():
    node = Node(
        icon="Ollama",
        name="Ollama LLM",
        items=[
            HandleElement(label="Cache", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(
                label="Base URL",
                placeholder="http://localhost:1234",
                type="url",
                hasHandle=True,
                handleStyle={"top": 104},
            ),
            DropdownItem(
                label="Model",
                options=["llama3", "llama2"],
                hasHandle=True,
                handleStyle={"top": 134},
            ),
            SliderItem(
                label="Temperature",
                min=0.0,
                max=2.0,
                step=0.01,
                initial=0.7,
                hasHandle=True,
                handleStyle={"top": 174},
            ),
            TextDisplay(text="Output"),
            HandleElement(
                label="Ollama",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node.json()
