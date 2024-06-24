import gradio as gr
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class Model(BaseModel):
    io: Any
    ELEMENTS_PER_ROW: int = 4
    stored_json: Optional[Dict[str, Any]] = None
    model_store: Dict[int, Dict[str, Any]] = {}

    def update_io(self, chat_interface: Optional[Any] = None, input_elements: Optional[List[Any]] = None, output_elements: Optional[List[Any]] = None):
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
        result = self.execute_model(*args)
        return result[0]
    
    def get_function(self, node: Dict[str, Any]):
        if node["Name"] == "Text Output":
            def function(data, *args):
                return data
            
        return function
