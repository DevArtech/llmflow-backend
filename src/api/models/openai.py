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
        # Santize the input data
        if isinstance(data, list) or isinstance(data, tuple):
            # Check to ensure that the first element is not an AIMessage
            if isinstance(data[0], AIMessage):
                raise ValueError("Cannot invoke LLM with AIMessage.")

            # If list is a conversation, invoke the model
            if isinstance(data[0], SystemMessage) or isinstance(data[0], HumanMessage):
                if len(data) > 1 and not isinstance(data[-1], HumanMessage):
                    if isinstance(data[-1], tuple):
                        data[-1] = HumanMessage(content=data[-1][0].strip())
                    else:
                        data[-1] = HumanMessage(content=data[-1].strip())

                return self.model.invoke(data)

            # If the list is not any of the above, just take the first element
            prompt = data[0]
        elif isinstance(data, dict):
            prompt = data["text"]
        else:
            prompt = data

        # Add the prompt to the cache and invoke the model
        conversation = self.cache + [HumanMessage(content=prompt.strip())]
        return self.model.invoke(conversation)
    
    class Config:
        protected_namespaces = ()
