from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from typing import Optional, List, Union
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class OpenAILLM(BaseModel):
    api_key: str
    model_type: str = "gpt-3.5-turbo-0125"
    temperature: float = 0.7
    model: ChatOpenAI = None
    cache: List[Union[HumanMessage, AIMessage, SystemMessage]] = []

    def __init__(
        self,
        api_key: str,
        model_type: str,
        temperature: float = 0.7,
        initial_cache: Optional[
            List[Union[SystemMessage, AIMessage, HumanMessage]]
        ] = None,
    ):
        super().__init__(
            api_key=api_key, model_type=model_type, temperature=temperature
        )
        self.model = ChatOpenAI(
            openai_api_key=api_key, model=model_type, temperature=temperature
        )

        if initial_cache is None:
            self.cache = [
                SystemMessage(
                    content="""You are an assistant developed by the LLMFlow framework. 
                         LLMFlow is a no-code framework that allows anyone to build an LLM application with ease. 
                         They can then take their generated programs to production with code generation and exportation to a Github repository."""
                )
            ]
        else:
            self.cache = initial_cache

    def invoke(self, data: str) -> AIMessage:
        if isinstance(data, list) or isinstance(data, tuple):
            prompt = data[0]
        elif isinstance(data, dict):
            prompt = data["text"]
        else:
            prompt = data

        conversation = self.cache + [HumanMessage(content=prompt.strip())]
        return self.model.invoke(conversation)
