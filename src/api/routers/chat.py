from fastapi import APIRouter, status
from ..modules.modules import (
    AvailableOptions,
    Node,
    HandleElement,
    TextDisplay,
    TextItem,
    CheckboxItem,
    Node,
)

router = APIRouter()


@router.get(
    "",
    summary="Get all available chat options",
    response_description="Return the available chat options",
    status_code=status.HTTP_200_OK,
    response_model=AvailableOptions,
)
async def get_chats():
    return AvailableOptions(
        options=[
            {"name": "Text-Chat", "detail": "Text-Only Chat Input/Output"},
            {"name": "Multimodal-Chat", "detail": " Multimodal Chat Input/Output"},
        ]
    )


@router.get(
    "/text-chat",
    summary="Get a text-based chat node",
    response_description="Return the text-based chat node",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_text_only_chat_node():
    node = Node(
        icon="Chat",
        name="Text-Only Chat",
        items=[
            HandleElement(label="Response", position="right", style={"top": 51}),
            TextDisplay(label="Input"),
            TextItem(label="Label", placeholder="Chat"),
            TextItem(label="Placeholder", placeholder=""),
            CheckboxItem(
                label="Right-To-Left", options={"labels": ["True"], "states": [False]}
            ),
            CheckboxItem(
                label="Rateable", options={"labels": ["True"], "states": [False]}
            ),
            TextDisplay(label="Output"),
            HandleElement(
                label="Prompt",
                position="left",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node


@router.get(
    "/multimodal-chat",
    summary="Get a multimodal chat node",
    response_description="Return the multimodal chat node",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_multimodal_chat_node():
    node = Node(
        icon="Chat",
        name="Multimodal Chat",
        items=[
            HandleElement(label="Response", position="right", style={"top": 51}),
            TextDisplay(label="Input"),
            TextItem(label="Label", placeholder="Chat"),
            TextItem(label="Placeholder", placeholder=""),
            CheckboxItem(
                label="Right-To-Left", options={"labels": ["True"], "states": [False]}
            ),
            CheckboxItem(
                label="Rateable", options={"labels": ["True"], "states": [False]}
            ),
            TextDisplay(label="Output"),
            HandleElement(
                label="Content",
                position="left",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node
