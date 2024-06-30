import json
import gradio as gr
from typing import Dict, List, Any, Optional
from api.modules.modules import *
from api.modules.model import Model
from fastapi import FastAPI, status, HTTPException
from api.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

CSS = """
#chat_texbox { flex-grow: 5; }
#chat_chatbot { height: 60vh !important; }
"""

app = FastAPI()
io = gr.Blocks(css=CSS)
model = Model()

ELEMENTS_PER_ROW = 4

def render_elements(chat_interface: Optional[Any] = None, input_elements: Optional[List[Any]] = None, output_elements: Optional[List[Any]] = None):
    io.clear()

    if input_elements == None:
        input_elements = [gr.Markdown(
            """
            # Welcome to LLMFlow!
            Add some input and output nodes to see the magic happen!
            """
        )]

    if output_elements == None:
        output_elements = []

    with io:
        if chat_interface:
            chat_interface.render()
        else:
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        if len(input_elements) > 0:
                            input_elements[0].render()
                    if len(input_elements) > 1:
                        for i in range(len(input_elements))[1::ELEMENTS_PER_ROW]:
                            with gr.Row():
                                for element in input_elements[i:i+ELEMENTS_PER_ROW]:
                                    element.render()
                        if chat_interface is None:
                            with gr.Row():
                                btn = gr.Button("Submit", size="sm", variant="primary")
                                btn.click(fn=model.execute_model, inputs=input_elements[1:], outputs=output_elements[1:])

                if chat_interface is None: 
                    with gr.Column():
                        with gr.Row():
                            if len(output_elements) > 0:
                                output_elements[0].render()
                        if len(output_elements) > 1:
                            for i in range(len(output_elements))[1::ELEMENTS_PER_ROW]:
                                with gr.Row():
                                    for element in output_elements[i:i+ELEMENTS_PER_ROW]:
                                        element.render()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", summary="Perform a Health Check", response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK, response_model=HealthCheck)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")

@app.get("/api/v1/integrations", summary="Get all available integrations", response_description="Return a list of all available integrations", status_code=status.HTTP_200_OK, response_model=AvailableIntegrations)
def get_integrations() -> AvailableIntegrations:
    """
    ## Get all available integrations
    Endpoint to get all available integrations that can be used in the LLMFlow.
    Returns:
        AvailableIntegrations: Returns a JSON response with all available integrations
    """
    return AvailableIntegrations(integrations=["Inputs", "Chat", "LLMs", "Outputs"])

@app.post("/api/v1/update-architecture", summary="Update the current Gradio architecture", response_description="Success on if the JSON is valid for the architecture", status_code=status.HTTP_200_OK)
def update_architecture(architecture: ArchitectureContract) -> Dict:
    """
    ## Update the current Gradio architecture
    Endpoint to update the current Gradio architecture with the JSON provided.
    Returns:
        Dict: Returns a JSON response with the success status
    """

    global input_elements, output_elements
    request_model = architecture.model
    if not model.compare_json(request_model):
        chat_interface = None
        input_elements = [gr.Markdown("# Input")]
        output_elements = [gr.Markdown("# Output")]
        elements = {}
        model_schema = {}
        
        if not request_model["Nodes"]:
            render_elements()
            return {"success": True}
        
        # try:
        for node in request_model["Nodes"]:
            if "Chat" in node["Name"]:
                input_elements.pop(0)
                # input_elements.insert(0, gr.Markdown("# Additional Inputs"))
                output_elements = None
                chat_obj = None
                if node["Name"] == "Text-Only Chat":
                    label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "Chat"
                    chat_obj = gr.ChatInterface(fn=model.execute_chat, multimodal=False, fill_height=True, additional_inputs=input_elements, chatbot=gr.Chatbot(
                        label=label,
                        rtl=node["Items"][2]["Value"],
                        likeable=node["Items"][3]["Value"],
                        elem_id="chat_chatbot"
                    ), textbox=gr.Textbox(placeholder=node["Items"][1]["Value"], rtl=node["Items"][2]["Value"], elem_id="chat_texbox"))

                if node["Name"] == "Multimodal Chat":
                    label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "Chat"
                    chat_obj = gr.ChatInterface(fn=model.execute_chat, multimodal=True, fill_height=True, chatbot=gr.Chatbot(
                        label=label,
                        rtl=node["Items"][2]["Value"],
                        likeable=node["Items"][3]["Value"],
                        elem_id="chat_chatbot"
                    ), textbox=gr.MultimodalTextbox(placeholder=node["Items"][1]["Value"], rtl=node["Items"][2]["Value"], elem_id="chat_multimodal"))
                
                chat_interface = chat_obj
                elements[node["Id"]] = chat_obj
            
            if "Input" in node["Name"]:
                input_obj = None
                if node["Name"] == "Text Input":
                    label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "Textbox"
                    input_obj = gr.Textbox(label=label, placeholder=node["Items"][1]["Value"], type=node["Items"][2]["Value"], elem_id=node["Id"])
                if node["Name"] == "Image Input":
                    label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "Image"
                    input_obj = gr.Image(label=label, elem_id=node["Id"])
                if node["Name"] == "Audio Input":
                    label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "Audio"
                    input_obj = gr.Audio(label=label, elem_id=node["Id"])
                if node["Name"] == "Video Input":
                    label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "Video"
                    input_obj = gr.Video(label=label, elem_id=node["Id"])                              
                if node["Name"] == "File Input":
                    label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "File"
                    input_obj = gr.File(label=label, elem_id=node["Id"])

                input_elements.append(input_obj)
                elements[node["Id"]] = input_obj

            if "LLM" in node["Name"]:
                llm_obj = None
                if node["Name"] == "OpenAI LLM":
                    llm_obj = gr.Textbox(visible=False, elem_id=node["Id"])

                elements[node["Id"]] = llm_obj

            elif "Output" in node["Name"]:
                output_obj = None
                if node["Name"] == "Text Output":
                    label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "Result"
                    output_obj = gr.Textbox(label=label, placeholder=node["Items"][1]["Value"], interactive=False, elem_id=node["Id"])
                    
                output_elements.append(output_obj)
                elements[node["Id"]] = output_obj

        for edge in request_model["Edges"]:
            source_node = request_model["Nodes"][int(edge["Source"]) - 1]
            source_element = elements[source_node["Id"]]
            target_node = request_model["Nodes"][int(edge["Target"]) - 1]

            func = model.get_function(target_node)

            if model_schema and source_element is model_schema[list(model_schema.keys())[-1]]["source"]:
                model_schema[list(model_schema.keys())[-1]]["func"].append(func)
            else:
                # target_node['Id'] only works for now so long as nodes only have one input. Should update later to handle multiple inputs
                model_schema[target_node['Id']] = {"source": source_element, "func": [func], "args": [target_node["Items"]], "overrides": []}

        for parameter_edge in request_model["ParameterEdges"]:
            source_node = request_model["Nodes"][int(parameter_edge["Source"]) - 1]
            source_element = elements[source_node["Id"]]
            target_node = request_model["Nodes"][int(parameter_edge["Target"]) - 1]

            item = model_schema[target_node['Id']]
            override = model.get_override(target_node, parameter_edge["Target Handle"])
            item["overrides"].append({override: input_elements.index(source_element) - 1 if chat_interface is None else input_elements.index(source_element)})
            model_schema[target_node['Id']] = item


        model.set_model(model_schema)
        model.store_json(request_model)

        # except Exception as e:
        #     raise HTTPException(status_code=400, detail=f"Invalid model architecture provided. Error: {e}")
        
        render_elements(chat_interface=chat_interface, input_elements=input_elements, output_elements=output_elements)
    return {"success": True}

render_elements()

app = gr.mount_gradio_app(app, io, path="/gradio")
app.include_router(api_router, prefix="/api/v1")
