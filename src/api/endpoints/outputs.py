from fastapi import APIRouter, status
from ..modules.modules import AvailableInputs, TextItem, DropdownItem, Node, NumberItem, TextDisplay, HandleElement

router = APIRouter()

@router.get("/", summary="Get all available output options", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK, response_model=AvailableInputs)
async def get_models():
    return AvailableInputs(inputs=["Text", "Image", "Audio", "Video", "File"])

@router.get("/text", summary="Get a text-based output node", response_description="Return the text-based output node", status_code=status.HTTP_200_OK)
async def get_text_output_node():
    node = Node(
        icon="Rtt",
        name="Text Output",
        items=[
            HandleElement(label="Text", position="left", style={"top": 51}),
        ]
    )

    return node.to_dict()