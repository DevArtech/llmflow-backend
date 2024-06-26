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
        return str(self.execute_model(args)[0])
    
    def get_function(self, node: Dict[str, Any]):
        if node["Name"] == "Text Output":
            def function(data, *args):
                return data
            
        return function
