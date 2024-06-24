from fastapi import APIRouter, status
from ..modules.modules import AvailableChatOptions, Node, HandleElement, TextDisplay, TextItem, CheckboxItem

router = APIRouter()

@router.get("/", summary="Get all available chat options", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK, response_model=AvailableChatOptions)
async def get_chats():
    return AvailableChatOptions(options=["Text-Chat", "Multimodal"])

@router.get("/text-chat", summary="Get a text-based chat node", response_description="Return the text-based chat node", status_code=status.HTTP_200_OK)
async def get_text_only_chat_node():
    node = Node(
        icon="Chat",
        name="Text-Only Chat Display Node",
        items=[
            HandleElement(label="Response", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="Label", placeholder="Chat"),
            TextItem(label="Placeholder", placeholder=""),
            CheckboxItem(label="Right-To-Left", options={"labels": ["True"], "states": [False]}),
            CheckboxItem(label="Copy", options={"labels": ["True"], "states": [False]}),
            CheckboxItem(label="Render Markdown", options={"labels": ["True"], "states": [True]}),
            CheckboxItem(label="Bubble Full Width", options={"labels": ["True"], "states": [True]}),
            CheckboxItem(label="Rateable", options={"labels": ["True"], "states": [False]}),
            TextDisplay(text="Output"),
            HandleElement(label="Prompt", position="right", type="source", style={"bottom": 12, "top": "auto"}),
        ]
    )

    return node.to_dict()