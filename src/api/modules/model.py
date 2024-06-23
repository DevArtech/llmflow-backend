from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class Model(BaseModel):
    model_store: Dict[int, Dict[str, Any]] = {}

    def set_model(self, model: List):
        self.model_store = model

    def get_model(self):
        return self.model_store
    
    def execute_model(self, *args):
        print(self.model_store)
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
    
    def get_function(self, node: Dict[str, Any]):
        if node["Name"] == "Text Output":
            def function(data, *args):
                return data
            
        return function
