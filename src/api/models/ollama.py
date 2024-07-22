from pydantic import BaseModel
from typing import Optional, List, Union
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class OllamaLLM(BaseModel):
    base_url: str = "http://localhost:11434"
    model_type: str = "llama3"
    temperature: float = 0.7
    system: str
    model: Ollama = None

    def __init__(
        self,
        base_url: str,
        model_type: str,
        system: str,
        temperature: float = 0.7,
    ):
        super().__init__(
            base_url=base_url, system=system, model_type=model_type, temperature=temperature
        )
        self.model = Ollama(
            base_url=base_url, system=system, model=model_type, temperature=temperature
        )

    def invoke(self, data: str) -> AIMessage:
        # Santize the input data
        if isinstance(data, list) or isinstance(data, tuple):
            data = data[0]
        return self.model.invoke(data)
        
