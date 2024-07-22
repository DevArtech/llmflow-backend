from fastapi import APIRouter, status
from ..modules.modules import (
    AvailableOptions,
    TextItem,
    DropdownItem,
    Node,
    Node,
    TextDisplay,
    HandleElement,
)

router = APIRouter()


@router.get(
    "",
    summary="Get all available input options",
    response_description="Return the available input options",
    status_code=status.HTTP_200_OK,
    response_model=AvailableOptions,
)
async def get_inputs():
    return AvailableOptions(
        options=[
            {"name": "Text", "detail": "Text Input"},
            {"name": "Image", "detail": "Image Input"},
            {"name": "Audio", "detail": "Audio Input"},
            {"name": "Video", "detail": "Video Input"},
            {"name": "File", "detail": "File Input"},
        ]
    )


@router.get(
    "/text",
    summary="Get a text-based input node",
    response_description="Return the text-based input node",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_text_input_node():
    node = Node(
        icon="Rtt",
        name="Text Input",
        items=[
            TextDisplay(label="Input"),
            TextItem(label="Label", placeholder="Textbox"),
            TextItem(label="Placeholder", placeholder=""),
            DropdownItem(
                label="Type", options=["text", "password", "email"], initial=0
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


@router.get(
    "/image",
    summary="Get a image-based input node",
    response_description="Return the image-based input node",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_image_input_node():
    node = Node(
        icon="Image",
        name="Image Input",
        items=[
            TextDisplay(label="Input"),
            TextItem(label="Label", placeholder="Image"),
            TextDisplay(label="Output"),
            HandleElement(
                label="Image",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node


@router.get(
    "/audio",
    summary="Get a audio-based input node",
    response_description="Return the audio-based input node",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_audio_input_node():
    node = Node(
        icon="Mic",
        name="Audio Input",
        items=[
            TextDisplay(label="Input"),
            TextItem(label="Label", placeholder="Audio"),
            TextDisplay(label="Output"),
            HandleElement(
                label="Audio",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node


@router.get(
    "/video",
    summary="Get a video-based input node",
    response_description="Return the video-based input node",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_video_input_node():
    node = Node(
        icon="Movie",
        name="Video Input",
        items=[
            TextDisplay(label="Input"),
            TextItem(label="Label", placeholder="Video"),
            TextDisplay(label="Output"),
            HandleElement(
                label="Video",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node


@router.get(
    "/file",
    summary="Get a file-based input node",
    response_description="Return the file-based input node",
    status_code=status.HTTP_200_OK,
    response_model=Node,
)
async def get_file_input_node():
    node = Node(
        icon="InsertDriveFile",
        name="File Input",
        items=[
            TextDisplay(label="Input"),
            TextItem(label="Label", placeholder="File"),
            TextDisplay(label="Output"),
            HandleElement(
                label="File",
                position="right",
                type="source",
                style={"bottom": 12, "top": "auto"},
            ),
        ],
    )

    return node
