from fastapi import APIRouter, status
from api.modules.modules import (
    AvailableOptions,
    Node,
    HandleElement,
    TextDisplay,
    TextItem,
    SliderItem,
    DropdownItem,
    Node,
)

router = APIRouter()


@router.get(
    "",
    summary="Get all available ROSIE options",
    response_description="Return the available ROSIE options",
    status_code=status.HTTP_200_OK,
    response_model=AvailableOptions,
)
async def get_rosie_nodes():
    return AvailableOptions(
        options=[
            {
                "name": "ROSIE LLM",
                "detail": "An LLM hosted on ROSIE, the MSOE Supercomputer.",
            },
            {
                "name": "ROSIE SKLearn",
                "detail": "An SKLearn model executed on ROSIE, the MSOE Supercomputer.",
            },
        ]
    )


@router.get(
    "/rosie-llm",
    summary="Get a ROSIE LLM node",
    response_description="Return the ROSIE LLM node",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_rosie_llm_node():
    node = Node(
        icon="FilterVintage",
        name="ROSIE LLM",
        items=[
            HandleElement(label="Cache", position="left", style={"top": 49}),
            TextDisplay(label="Input"),
            DropdownItem(
                label="Model",
                options=["llama3-8b", "llama2-7b", "mistral-7b"],
                hasHandle=True,
                handleStyle={"top": 100},
            ),
            SliderItem(
                label="Temperature",
                min=0.0,
                max=2.0,
                step=0.01,
                initial=0.7,
                hasHandle=True,
                handleStyle={"bottom": 70, "top": "auto"},
            ),
            TextDisplay(label="Output"),
            HandleElement(
                label="Response",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node


@router.get(
    "/rosie-sklearn",
    summary="Get a ROSIE SKLearn node",
    response_description="Return the ROSIE SKLearn node",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_rosie_sklearn_node():
    node = Node(
        icon="FilterVintage",
        name="ROSIE SKLearn",
        items=[
            HandleElement(label="Input", position="left", style={"top": 49}),
            TextDisplay(label="Input"),
            TextItem(label="Prompt", placeholder=""),
            TextItem(label="Model", placeholder=""),
            TextDisplay(label="Output"),
            HandleElement(
                label="Response",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node
