from fastapi import APIRouter, status
from ..modules.modules import AvailableChatOptions, Node, HandleElement, TextDisplay, TextItem, CheckboxItem

router = APIRouter()

@router.get("/", summary="Get all available chat options", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK, response_model=AvailableChatOptions)
async def get_chats():
    return AvailableChatOptions(options=["Text-Chat", "Multimodal-Chat"])

@router.get("/text-chat", summary="Get a text-based chat node", response_description="Return the text-based chat node", status_code=status.HTTP_200_OK)
async def get_text_only_chat_node():
    node = Node(
        icon="Chat",
        name="Text-Only Chat Display Node",
        items=[
            HandleElement(label="Response", position="right", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="Label", placeholder="Chat"),
            TextItem(label="Placeholder", placeholder=""),
            CheckboxItem(label="Right-To-Left", options={"labels": ["True"], "states": [False]}),
            CheckboxItem(label="Rateable", options={"labels": ["True"], "states": [False]}),
            TextDisplay(text="Output"),
            HandleElement(label="Prompt", position="left", type="source", style={"bottom": 12, "top": "auto"}),
        ]
    )

    return node.to_dict()

@router.get("/multimodal-chat", summary="Get a multimodal chat node", response_description="Return the multimodal chat node", status_code=status.HTTP_200_OK)
async def get_multimodal_chat_node():
    node = Node(
        icon="Chat",
        name="Multimodal Chat Display Node",
        items=[
            HandleElement(label="Response", position="right", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="Label", placeholder="Chat"),
            TextItem(label="Placeholder", placeholder=""),
            CheckboxItem(label="Right-To-Left", options={"labels": ["True"], "states": [False]}),
            CheckboxItem(label="Rateable", options={"labels": ["True"], "states": [False]}),
            TextDisplay(text="Output"),
            HandleElement(label="Content", position="left", type="source", style={"bottom": 12, "top": "auto"}),
        ]
    )

    return node.to_dict()