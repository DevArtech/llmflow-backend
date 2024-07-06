import json
from pydantic import BaseModel
from typing import List, Dict, Optional, Any, Union
from enum import Enum


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


class AvailableOptions(BaseModel):
    """Response model to validate and return all available options under an endpoint."""

    options: Union[List[str], List[Dict[str, str]]] = [
        "Text-Chat",
        "Multimodal",
        "Text",
        "Image",
        "Audio",
        "Video",
        "File",
    ]


class AvailableIntegrations(BaseModel):
    """Contract model to validate and return all available integrations."""

    integrations: List[str] = ["Inputs", "LLMs", "Outputs"]


class ArchitectureContract(BaseModel):
    """Contract model to update the architecture of the Gradio application."""

    model: Dict[str, Any]


class NodeItem(BaseModel):
    """An element of the node object."""

    label: str = ""
    required: Optional[bool] = False
    hasHandle: Optional[bool] = False
    handleType: Optional[str] = "target"
    handlePosition: Optional[str] = "left"
    handleStyle: Optional[Dict[str, Any]] = {}

    def to_dict(self):
        raise NotImplementedError("Method to_dict not implemented")


class Node(BaseModel):
    """Base model to get the JSON of a node"""

    icon: Optional[str] = None
    name: Optional[str] = None
    items: Optional[List[Union[NodeItem]]] = None

    def json(self, **kwargs) -> Dict[str, Any]:
        node_items = [item.to_dict() for item in self.items] if self.items else []
        return {"icon": self.icon, "name": self.name, "items": node_items}


class HandleElement(NodeItem):
    """Handle element for the node object."""

    type: str = "target"
    position: str = "left"
    style: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "handle": {
                "label": self.label,
                "type": self.type,
                "position": self.position,
                "style": self.style,
            }
        }


class TextDisplay(NodeItem):
    """Non-interactable text display item for the node object."""

    text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"text-display": {"text": self.text}}


class TextItem(NodeItem):
    """Text item for the node object."""

    placeholder: str = ""
    type: str = "text"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": {
                "label": self.label,
                "required": self.required,
                "placeholder": self.placeholder,
                "type": self.type,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class TextAreaItem(NodeItem):
    """Text area item for the node object."""

    placeholder: str = ""
    type: str = "text"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text-area": {
                "label": self.label,
                "required": self.required,
                "placeholder": self.placeholder,
                "type": self.type,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class FileItem(NodeItem):
    """File item for the node object."""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file": {
                "label": self.label,
                "required": self.required,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class RadioItem(NodeItem):
    """Radio item for the node object."""

    options: List[str]
    initial: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "radio": {
                "label": self.label,
                "required": self.required,
                "options": self.options,
                "initial": self.initial,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class ColorItem(NodeItem):
    """Color item for the node object."""

    initial: str = "#000000"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "color": {
                "label": self.label,
                "required": self.required,
                "initial": self.initial,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class SliderItem(NodeItem):
    """Slider item for the node object."""

    min: float = 0
    max: float = 1
    step: float = 0.01
    initial: float = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slider": {
                "label": self.label,
                "required": self.required,
                "min": self.min,
                "max": self.max,
                "step": self.step,
                "initial": self.initial,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class DropdownItem(NodeItem):
    """Dropdown item for the node object."""

    options: List[str]
    initial: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dropdown": {
                "label": self.label,
                "required": self.required,
                "options": self.options,
                "initial": self.initial,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class CheckboxItem(NodeItem):
    """Checkbox item for the node object."""

    options: Dict[str, List[Any]] = {"labels": ["A"], "states": [True]}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "checkbox": {
                "label": self.label,
                "required": self.required,
                "options": self.options,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class BezierCurveItem(NodeItem):
    """Bezier Curve item for the node object."""

    initialHandles: List[Dict[str, int]]
    maxX: int = 300
    maxY: int = 200

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bezier": {
                "label": self.label,
                "required": self.required,
                "initialHandles": self.initialHandles,
                "maxX": self.maxX,
                "maxY": self.maxY,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class DatetimeItem(NodeItem):
    """Datetime item for the node object."""

    initial: str = "2024-05-09T21:35"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "datetime": {
                "label": self.label,
                "required": self.required,
                "initial": self.initial,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class NumberItem(NodeItem):
    """Number item for the node object."""

    min: float = 0
    max: float = 100
    step: float = 1
    initial: float = 50

    def to_dict(self) -> Dict[str, Any]:
        return {
            "number": {
                "label": self.label,
                "required": self.required,
                "min": self.min,
                "max": self.max,
                "step": self.step,
                "initial": self.initial,
                "hasHandle": self.hasHandle,
                "handleType": self.handleType,
                "handlePosition": self.handlePosition,
                "handleStyle": self.handleStyle,
            }
        }


class NodeContract(BaseModel):
    """Contract model for a node."""

    icon: Optional[str] = None
    name: Optional[str] = None
    items: Optional[List[Dict[str, Union[Any, NodeItem]]]] = None

    def json(self):
        raise NotImplementedError("Method to_dict not implemented")
