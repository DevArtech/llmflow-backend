import json
import gradio as gr
from pydantic import BaseModel
from typing import List, Dict, Optional, Any, Union, Callable


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


class AvailableOptions(BaseModel):
    """Response model to validate and return all available options under an endpoint."""

    options: Union[List[Dict[str, str]]] = [
        {"name": "Text-Chat", "details": "Text-Only Chat Input/Output"},
        {"name": "Multimodal", "details": "Multimodal Chat Input/Output"},
        {"name": "Text", "details": "Text Input"},
        {"name": "Image", "details": "Image Input"},
        {"name": "OpenAI", "details": "OpenAI LLM"},
        {"name": "Video", "details": "Video Output"},
        {"name": "File", "details": "File Output"},
    ]


class AvailableIntegrations(BaseModel):
    """Contract model to validate and return all available integrations."""

    integrations: List[str] = ["Inputs", "LLMs", "Outputs"]


class ArchitectureContract(BaseModel):
    """Contract model to update the architecture of the Gradio application."""

    model: Dict[str, Any]


class NodeItem(BaseModel):
    """An element of the node object."""

    itemType: str = "text"
    label: str = ""
    required: Optional[bool] = False
    hasHandle: Optional[bool] = False
    handleType: Optional[str] = "target"
    handlePosition: Optional[str] = "left"
    handleStyle: Optional[Dict[str, Any]] = {}


class HandleElement(NodeItem):
    """Handle element for the node object."""

    itemType: str = "handle"
    type: str = "target"
    position: str = "left"
    style: Dict[str, Any] = {}


class TextDisplay(NodeItem):
    """Non-interactable text display item for the node object."""

    itemType: str = "text-display"


class TextItem(NodeItem):
    """Text item for the node object."""

    placeholder: str = ""
    type: str = "text"


class TextAreaItem(NodeItem):
    """Text area item for the node object."""

    itemType: str = "text-area"
    placeholder: str = ""
    type: str = "text"


class FileItem(NodeItem):
    """File item for the node object."""

    itemType: str = "file"


class RadioItem(NodeItem):
    """Radio item for the node object."""

    itemType: str = "radio"
    options: List[str]
    initial: int = 0


class ColorItem(NodeItem):
    """Color item for the node object."""

    itemType: str = "color"
    initial: str = "#000000"


class SliderItem(NodeItem):
    """Slider item for the node object."""

    itemType: str = "slider"
    min: float = 0
    max: float = 1
    step: float = 0.01
    initial: float = 0


class DropdownItem(NodeItem):
    """Dropdown item for the node object."""

    itemType: str = "dropdown"
    options: List[str]
    initial: int = 0


class CheckboxItem(NodeItem):
    """Checkbox item for the node object."""

    itemType: str = "checkbox"
    options: Dict[str, List[Any]] = {"labels": ["A"], "states": [True]}


class BezierCurveItem(NodeItem):
    """Bezier Curve item for the node object."""

    itemType: str = "bezier"
    initialHandles: List[Dict[str, int]]
    maxX: int = 300
    maxY: int = 200


class DatetimeItem(NodeItem):
    """Datetime item for the node object."""

    itemType: str = "datetime"
    initial: str = "2024-05-09T21:35"


class NumberItem(NodeItem):
    """Number item for the node object."""

    itemType: str = "number"
    min: float = 0
    max: float = 100
    step: float = 1
    initial: float = 50


class Node(BaseModel):
    """Base model to get the JSON of a node"""

    icon: Optional[str] = None
    name: Optional[str] = None
    items: Optional[
        List[
            NodeItem
            | Union[
                HandleElement,
                TextDisplay,
                TextItem,
                TextAreaItem,
                FileItem,
                RadioItem,
                ColorItem,
                SliderItem,
                DropdownItem,
                CheckboxItem,
                BezierCurveItem,
                DatetimeItem,
                NumberItem,
            ]
        ]
    ] = None


class ModelNode(BaseModel):
    """A node in a list of nodes."""

    idx: int
    name: str
    sources: List[int]
    func: List[Callable]
    args: List[Dict[str, Any]]
    overrides: Optional[List[Dict[str, int]]] = None
