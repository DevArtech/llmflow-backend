import json
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""
    status: str = "OK"

class AvailableLLMs(BaseModel):
    models: List[str] = ["OpenAI", "Gemini", "Ollama"]

class AvailableInputs(BaseModel):
    inputs: List[str] = ["Text", "Image", "Audio", "Video", "File"]

class AvailableOutputs(BaseModel):
    inputs: List[str] = ["Text", "Image", "Audio", "Video", "File"]

class NodeItem(BaseModel):
    """An element of the node object."""
    label: str = ""

    def to_dict(self):
        pass

class Node(BaseModel):
    """Contract model to get the JSON of a node"""
    icon: Optional[str] = None
    name: Optional[str] = None
    items: Optional[List[NodeItem]] = None

    def to_dict(self):
        node_items = []
        for item in self.items:
            node_items.append(item.to_dict())

        return {
            "icon": self.icon,
            "name": self.name,
            "items": node_items
        }
    
class HandleElement(NodeItem):
    """Handle element for the node object."""
    type: str = "target"
    position: str = "left"
    style: Dict[str, Any] = {}

    def to_dict(self):
        return {"handle": {
            "label": self.label,
            "type": self.type,
            "position": self.position,
            "style": self.style
        }}

class TextDisplay(NodeItem):
    """Non-interactable text display item for the node object."""
    text: str = ""

    def to_dict(self):
        return {"text-display": {
            "text": self.text
        }}

class TextItem(NodeItem):
    """Text item for the node object."""
    placeholder: str = ""
    type: str = "text"

    def to_dict(self):
        return {"text": {
            "label": self.label,
            "placeholder": self.placeholder,
            "type": self.type
        }}

class FileItem(NodeItem):
    """File item for the node object."""

    def to_dict(self):
        return {"file": {
            "label": self.label
        }}

class RadioItem(NodeItem):
    """Radio item for the node object."""
    options: List[str]
    initial: int = 0

    def to_dict(self):
        return {"radio": {
            "label": self.label,
            "options": self.options,
            "initial": self.initial
        }}

class ColorItem(NodeItem):
    """Color item for the node object."""
    initial: str = "#000000"

    def to_dict(self):
        return {"color": {
            "label": self.label,
            "initial": self.initial
        }}

class SliderItem(NodeItem):
    """Slider item for the node object."""
    min: float = 0
    max: float = 1
    step: float = 0.01
    initial: float = 0

    def to_dict(self):
        return {"slider": {
            "label": self.label,
            "min": self.min,
            "max": self.max,
            "step": self.step,
            "initial": self.initial
        }}

class DropdownItem(NodeItem):
    """Dropdown item for the node object."""
    options: List[str]
    initial: int = 0

    def to_dict(self):
        return {"dropdown": {
            "label": self.label,
            "options": self.options,
            "initial": self.initial
        }}

class CheckboxItem(NodeItem):
    """Checkbox item for the node object."""
    options: Dict[str, bool] = [{"A": True}]

    def to_dict(self):
        return {"checkbox": {
            "label": self.label,
            "options": self.options
        }}

class BezierCurveItem(NodeItem):
    """Bezier Curve item for the node object."""
    initialHandles: List[Dict[str, int]]
    maxX: int = 300
    maxY: int = 200

    def to_dict(self):
        return {"bezier": {
            "label": self.label,
            "initialHandles": self.initialHandles,
            "maxX": self.maxX,
            "maxY": self.maxY
        }}

class DatetimeItem(NodeItem):
    """Datetime item for the node object."""
    initial: str = "2024-05-09T21:35"

    def to_dict(self):
        return {"datetime": {
            "label": self.label,
            "initial": self.initial
        }}

class NumberItem(NodeItem):
    """Number item for the node object."""
    min: float = 0
    max: float = 100
    step: float = 1
    initial: float = 50

    def to_dict(self):
        return {"number": {
            "label": self.label,
            "min": self.min,
            "max": self.max,
            "step": self.step,
            "initial": self.initial
        }}