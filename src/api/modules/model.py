import gradio as gr
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from ..models.llms.openai import OpenAILLM
from langchain_core.messages import SystemMessage

class Model(BaseModel):
    io: Any
    ELEMENTS_PER_ROW: int = 4
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
    
    def render_elements(self, chat_interface: Optional[Any] = None, input_elements: Optional[List[Any]] = None, output_elements: Optional[List[Any]] = None):
        self.io.clear()

        if input_elements == None:
            input_elements = [gr.Markdown(
                """
                # Welcome to LLMFlow!
                Add some input and output nodes to see the magic happen!
                """
            )]

        if output_elements == None:
            output_elements = []

        with self.io:
            if chat_interface:
                chat_interface.render()
            else:
                with gr.Row():
                    with gr.Column():
                        with gr.Row():
                            if len(input_elements) > 0:
                                input_elements[0].render()
                        if len(input_elements) > 1:
                            for i in range(len(input_elements))[1::self.ELEMENTS_PER_ROW]:
                                with gr.Row():
                                    for element in input_elements[i:i+self.ELEMENTS_PER_ROW]:
                                        element.render()
                            if chat_interface is None:
                                with gr.Row():
                                    btn = gr.Button("Submit", size="sm", variant="primary")
                                    btn.click(fn=self.execute_model, inputs=input_elements[1:], outputs=output_elements[1:])

                    if chat_interface is None: 
                        with gr.Column():
                            with gr.Row():
                                if len(output_elements) > 0:
                                    output_elements[0].render()
                            if len(output_elements) > 1:
                                for i in range(len(output_elements))[1::self.ELEMENTS_PER_ROW]:
                                    with gr.Row():
                                        for element in output_elements[i:i+self.ELEMENTS_PER_ROW]:
                                            element.render()
    
    def execute_model(self, *args):
        data = args
        for i, value in self.model_store.items():
            if value["overrides"]:
                for override in value["overrides"]:
                    ovrd_key = list(override.keys())[0]
                    ovrd_value = int(override[ovrd_key])
                    for dictionary in value["args"][0]:
                        if "Type" in dictionary and dictionary["Type"] == ovrd_key:
                            if isinstance(args[0], tuple):
                                dictionary["Value"] = args[0][ovrd_value + 2]
                            else:
                                dictionary["Value"] = args[ovrd_value]
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
        if not self.model_store:
            return "Chat interface is not connected to any output. Please loop the chat interface to reconnect to itself via other nodes or itself."
        
        response = self.execute_model(args)

        if isinstance(response, tuple) and isinstance(response[0], dict):
            res = response[0].copy()
            response = ""
            for key, value in res.items():
                if key == "text":
                    response += value
                if key == "files":
                    if len(value) > 0:
                        response += " - Files: "
                    for file in value:
                        response += f"{file}\n"
            
        return str(response[0]) if isinstance(response, list) or isinstance(response, tuple) else str(response)
    
    def get_function(self, node: Dict[str, Any]):
        if node["Name"] == "OpenAI LLM":
            def function(data, *args):
                initial_cache = None
                if args[0][3]["Value"] != "":
                    initial_cache = [SystemMessage(content=args[0][3]["Value"])]
                model = OpenAILLM(api_key=args[0][0]["Value"], model_type=args[0][1]["Value"], temperature=float(args[0][2]["Value"]), initial_cache=initial_cache)
                return model.invoke(data).content
        else:
            def function(data, *args):
                return data
            
        return function
    
    def get_override(self, node: Dict[str, Any], handle: str):
        if node["Name"] == "OpenAI LLM":
            if handle == "element_2":
                return "API Key"
            if handle == "element_3":
                return "Model"
            if handle == "element_4":
                return "Temperature"
            if handle == "element_5":
                return "System Message"

