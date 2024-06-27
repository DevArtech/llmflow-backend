from openai import OpenAI
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class Model(BaseModel):
    stored_json: Optional[Dict[str, Any]] = None
    model_store: Dict[int, Dict[str, Any]] = {}

    def store_json(self, json_data: Dict[str, Any]):
        self.stored_json = json_data

    def compare_json(self, json_data: Dict[str, Any]):
        if self.stored_json == None:
            return False

        return self.stored_json == json_data

    def set_model(self, model: List):
        self.model_store = model

    def get_model(self):
        return self.model_store
    
    def execute_model(self, *args):
        data = args
        for _, value in self.model_store.items():
            final_result = []
            for idx, func in enumerate(value["func"]):
                temp_data = None
                if type(data) == list or type(data) == tuple:
                    try:
                        temp_data = func(data[idx], *value["args"])
                    except IndexError:
                        temp_data = func(data[0], *value["args"])
                else:
                    temp_data = func(data, *value["args"])
                final_result.append(temp_data)
            
            data = final_result

        if len(data) == 1:
            return data[0]
        
        return data
    
    def execute_chat(self, *args):
        response = self.execute_model(args)
        return str(response[0]) if isinstance(response, list) or isinstance(response, tuple) else str(response)
    
    def get_function(self, node: Dict[str, Any]):
        if node["Name"] == "OpenAI LLM":
            def function(data, *args):
                client = OpenAI(api_key=args[0][0]["Value"])
                completion = client.chat.completions.create(
                    model=args[0][1]["Value"],
                    messages=[
                        {"role": "system", "content": """You are an assistant developed by the LLMFlow framework. 
                         LLMFlow is a no-code framework that allows anyone to build an LLM application with ease. 
                         They can then take their generated programs to production with code generation and exportation to a Github repository."""},
                        {"role": "user", "content": data[0]}
                    ],
                    temperature=float(args[0][2]["Value"])
                )
                print(completion.choices[0].message.content)
                return completion.choices[0].message.content
        else:
            def function(data, *args):
                return data
            
        return function
