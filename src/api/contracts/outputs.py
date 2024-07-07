from fastapi import APIRouter, status
from ..modules.modules import (
    AvailableOptions,
    TextItem,
    DropdownItem,
    Node,
    NumberItem,
    TextDisplay,
    HandleElement,
    NodeContract,
)

router = APIRouter()


@router.get(
    "/",
    summary="Get all available output options",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=AvailableOptions,
)
async def get_outputs():
    return AvailableOptions(
        options=[
            {"name": "Text", "detail": "Text Output"},
            {"name": "Image", "detail": "Image Output"},
            {"name": "Audio", "detail": "Audio Output"},
            {"name": "Video", "detail": "Video Output"},
            {"name": "File", "detail": "File Output"},
        ]
    )


@router.get(
    "/text",
    summary="Get a text-based output node",
    response_description="Return the text-based output node",
    status_code=status.HTTP_200_OK,
    response_model=NodeContract,
)
async def get_text_output_node():
    node = Node(
        icon="Rtt",
        name="Text Output",
        items=[
            HandleElement(label="Text", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="Label", placeholder="Textbox"),
            TextItem(label="Placeholder", placeholder=""),
        ],
    )

    return node.json()


@router.get(
    "/image",
    summary="Get a image-based output node",
    response_description="Return the image-based output node",
    status_code=status.HTTP_200_OK,
    response_model=NodeContract,
)
async def get_image_output_node():
    node = Node(
        icon="Image",
        name="Image Output",
        items=[
            HandleElement(label="Text", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="Label", placeholder="Image"),
        ],
    )

    return node.json()


@router.get(
    "/audio",
    summary="Get a audio-based output node",
    response_description="Return the audio-based output node",
    status_code=status.HTTP_200_OK,
    response_model=NodeContract,
)
async def get_audio_output_node():
    node = Node(
        icon="Mic",
        name="Audio Output",
        items=[
            HandleElement(label="Text", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="Label", placeholder="Audio"),
        ],
    )

    return node.json()


@router.get(
    "/video",
    summary="Get a video-based output node",
    response_description="Return the video-based output node",
    status_code=status.HTTP_200_OK,
    response_model=NodeContract,
)
async def get_video_output_node():
    node = Node(
        icon="Movie",
        name="Video Output",
        items=[
            HandleElement(label="Text", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="Label", placeholder="Video"),
        ],
    )

    return node.json()


@router.get(
    "/file",
    summary="Get a file-based output node",
    response_description="Return the file-based output node",
    status_code=status.HTTP_200_OK,
    response_model=NodeContract,
)
async def get_file_output_node():
    node = Node(
        icon="InsertDriveFile",
        name="File Output",
        items=[
            HandleElement(label="Text", position="left", style={"top": 51}),
            TextDisplay(text="Input"),
            TextItem(label="Label", placeholder="File"),
        ],
    )

    return node.json()
