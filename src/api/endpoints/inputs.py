from fastapi import APIRouter, status
from ..modules.modules import AvailableInputs, TextItem, DropdownItem, Node, NumberItem, TextDisplay, HandleElement

router = APIRouter()

@router.get("/", summary="Get all available input options", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK, response_model=AvailableInputs)
async def get_models():
    return AvailableInputs(inputs=["Text", "Image", "Audio", "Video", "File"])

@router.get("/text", summary="Get a text-based input node", response_description="Return the text-based input node", status_code=status.HTTP_200_OK)
async def get_text_input_node():
    node = Node(
        icon="Rtt",
        name="Text Input",
        items=[
            TextDisplay(text="Input"),
            TextItem(label="Placeholder", placeholder=""),
            TextDisplay(text="Output"),
            HandleElement(label="Prompt", position="right", type="source", style={"bottom": 12, "top": "auto"}),
        ]
    )

    return node.to_dict()