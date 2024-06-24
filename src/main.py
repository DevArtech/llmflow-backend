import json
import gradio as gr
from typing import Dict, List, Any, Optional
from api.modules.modules import *
from api.modules.model import Model
from fastapi import FastAPI, status, HTTPException
from api.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
model = Model(io=gr.Blocks())

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
            model.update_io()
            return {"success": True}
        
        # try:
        for node in request_model["Nodes"]:
            if "Chat" in node["Name"]:
                input_elements.pop(0)
                input_elements.insert(0, gr.Markdown("# Additional Inputs"))
                output_elements = None
                chat_obj = None
                label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "Chat"
                print(label)
                chatbot = gr.Chatbot(label=label,
                                        rtl=node["Items"][2]["Value"],
                                        show_copy_button=node["Items"][3]["Value"],
                                        render_markdown=node["Items"][4]["Value"],
                                        bubble_full_width=node["Items"][5]["Value"],
                                        likeable=node["Items"][6]["Value"],
                                        elem_id=f"chattext_1")
                textbox = gr.Textbox(label=None, placeholder=node["Items"][1]["Value"], elem_id=f"chattext_2")
                chat_obj = gr.ChatInterface(fn=model.execute_chat, multimodal=False if node["Name"] == "Text-Only Chat Display Node" else True, fill_height=True, chatbot=chatbot, textbox=textbox)
                
                chat_interface = chat_obj
                elements[node["Id"]] = chat_obj
            
            if "Input" in node["Name"]:
                input_obj = None
                if node["Name"] == "Text Input":
                    label = node["Items"][0]["Value"] if node["Items"][0]["Value"] != "" else "Textbox"
                    input_obj = gr.Textbox(label=label, placeholder=node["Items"][1]["Value"], elem_id=node["Id"])
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
            target_element = elements[target_node["Id"]]

            func = model.get_function(target_node)

            if model_schema and source_element is model_schema[list(model_schema.keys())[-1]]["source"]:
                model_schema[list(model_schema.keys())[-1]]["func"].append(func)
            else:
                idx = len(model_schema)
                model_schema[idx] = {"source": source_element, "func": [func], "args": []}

        model.set_model(model_schema)
        model.store_json(request_model)

        # except Exception as e:
        #     raise HTTPException(status_code=400, detail=f"Invalid model architecture provided. Error: {e}")
        
        model.update_io(chat_interface=chat_interface, input_elements=input_elements, output_elements=output_elements)
    return {"success": True}

@app.get("/api/v1/reset-architecture", summary="Reset the current Gradio architecture", response_description="Success on if the architecture is reset", status_code=status.HTTP_200_OK)
async def reset_architecture():
    global model
    model = Model()
    return {"success": True}

app = gr.mount_gradio_app(app, model.io, path="/gradio")
app.include_router(api_router, prefix="/api/v1")
