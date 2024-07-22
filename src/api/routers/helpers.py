from fastapi import APIRouter, status
from ..modules.modules import (
    AvailableOptions,
    Node,
    HandleElement,
    TextDisplay,
    TextItem,
    CheckboxItem,
    TextAreaItem,
    Node,
)

router = APIRouter()


@router.get(
    "",
    summary="Get all available helper functions.",
    response_description="Return the available helper functions.",
    status_code=status.HTTP_200_OK,
    response_model=AvailableOptions,
)
async def get_helpers():
    return AvailableOptions(
        options=[
            {"name": "System Prompt", "detail": "System Prompt"},
            {"name": "Chat Constructor", "detail": "Chat Constructor"},
        ]
    )


@router.get(
    "/system-prompt",
    summary="Get a system prompt node.",
    response_description="Return the system prompt node.",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_system_prompt_node():
    node = Node(
        icon="Terminal",
        name="System Prompt",
        items=[
            TextDisplay(label="Input"),
            TextAreaItem(
                label="Prompt",
                placeholder="You are a helpful agent.",
                required=True,
                hasHandle=True,
                handleStyle={"top": 81},
            ),
            TextDisplay(label="Output"),
            HandleElement(
                label="Prompt",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )
    return node
