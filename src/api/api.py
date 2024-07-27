import os
import configparser
from fastapi import APIRouter, Response, status, HTTPException

from api.modules.modules import *
from api.modules.model import Model
from middleware.logging_middleware import logger
from .routers import llms, inputs, outputs, chat, helpers

addons = []
try:
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    addons = config["settings"]["addons"].split(",")
except NameError:
    pass
except KeyError:
    pass

CSS = """
#chat_texbox { flex-grow: 5; }
#chat_chatbot { height: 60vh !important; }
"""

router = APIRouter()

model = Model(io=gr.Blocks(css=CSS))


@router.get(
    "/integrations",
    summary="Get all available integrations",
    response_description="Return a list of all available integrations",
    response_model=AvailableIntegrations,
)
def get_integrations() -> AvailableIntegrations:
    """
    ## Get all available integrations
    Endpoint to get all available integrations that can be used in the LLMFlow.
    Returns:
    - AvailableIntegrations: Returns a JSON response with all available integrations
    """
    integrations = ["Inputs", "Chat", "LLMs", "Helpers", "Outputs"]
    if "ROSIE" in addons:
        integrations.insert(-2, "ROSIE")
    return AvailableIntegrations(integrations=integrations)


@router.post(
    "/update-architecture",
    summary="Update the current Gradio architecture",
    response_description="Success on if the JSON is valid for the architecture",
    response_model=None,
)
def update_architecture(architecture: ArchitectureContract) -> None:
    """
    ## Update the current Gradio architecture
    Endpoint to update the current Gradio architecture with the JSON provided.
    Returns:
    - Dict: Returns a JSON response with the success status
    """

    request_model = architecture.model
    if not model.compare_json(request_model):
        chat_interface = None
        input_elements = [gr.Markdown("# Input")]
        output_elements = [gr.Markdown("# Output")]
        elements = {}
        model_schema: List = []

        if not request_model.get("Nodes") or not request_model.get("Edges"):
            model.render_elements()
            return {"success": True}

        try:
            for node in request_model["Nodes"]:
                if "Chat" in node["Name"]:
                    input_elements.pop(0)
                    output_elements = None
                    chat_obj = None
                    if node["Name"] == "Text-Only Chat":
                        label = (
                            node["Items"][0]["Value"]
                            if node["Items"][0]["Value"] != ""
                            else "Chat"
                        )
                        chat_obj = gr.ChatInterface(
                            fn=model.execute_chat,
                            multimodal=False,
                            fill_height=True,
                            additional_inputs=input_elements,
                            chatbot=gr.Chatbot(
                                label=label,
                                rtl=node["Items"][2]["Value"],
                                likeable=node["Items"][3]["Value"],
                                elem_id="chat_chatbot",
                            ),
                            textbox=gr.Textbox(
                                placeholder=node["Items"][1]["Value"],
                                rtl=node["Items"][2]["Value"],
                                elem_id="chat_texbox",
                            ),
                        )

                    if node["Name"] == "Multimodal Chat":
                        label = (
                            node["Items"][0]["Value"]
                            if node["Items"][0]["Value"] != ""
                            else "Chat"
                        )
                        chat_obj = gr.ChatInterface(
                            fn=model.execute_chat,
                            multimodal=True,
                            fill_height=True,
                            chatbot=gr.Chatbot(
                                label=label,
                                rtl=node["Items"][2]["Value"],
                                likeable=node["Items"][3]["Value"],
                                elem_id="chat_chatbot",
                            ),
                            textbox=gr.MultimodalTextbox(
                                placeholder=node["Items"][1]["Value"],
                                rtl=node["Items"][2]["Value"],
                                elem_id="chat_multimodal",
                            ),
                        )

                    chat_interface = chat_obj
                    elements[node["Id"]] = chat_obj

                if "Input" in node["Name"]:
                    input_obj = None
                    if node["Name"] == "Text Input":
                        label = (
                            node["Items"][0]["Value"]
                            if node["Items"][0]["Value"] != ""
                            else "Textbox"
                        )
                        input_obj = gr.Textbox(
                            label=label,
                            placeholder=node["Items"][1]["Value"],
                            type=node["Items"][2]["Value"],
                            elem_id=node["Id"],
                        )
                    if node["Name"] == "Image Input":
                        label = (
                            node["Items"][0]["Value"]
                            if node["Items"][0]["Value"] != ""
                            else "Image"
                        )
                        input_obj = gr.Image(label=label, elem_id=node["Id"])
                    if node["Name"] == "Audio Input":
                        label = (
                            node["Items"][0]["Value"]
                            if node["Items"][0]["Value"] != ""
                            else "Audio"
                        )
                        input_obj = gr.Audio(label=label, elem_id=node["Id"])
                    if node["Name"] == "Video Input":
                        label = (
                            node["Items"][0]["Value"]
                            if node["Items"][0]["Value"] != ""
                            else "Video"
                        )
                        input_obj = gr.Video(label=label, elem_id=node["Id"])
                    if node["Name"] == "File Input":
                        label = (
                            node["Items"][0]["Value"]
                            if node["Items"][0]["Value"] != ""
                            else "File"
                        )
                        input_obj = gr.File(label=label, elem_id=node["Id"])

                    input_elements.append(input_obj)
                    elements[node["Id"]] = input_obj

                if "LLM" in node["Name"]:
                    llm_obj = gr.Textbox(visible=False, elem_id=node["Id"])
                    elements[node["Id"]] = llm_obj

                elif "Output" in node["Name"]:
                    output_obj = None
                    if node["Name"] == "Text Output":
                        label = (
                            node["Items"][0]["Value"]
                            if node["Items"][0]["Value"] != ""
                            else "Result"
                        )
                        output_obj = gr.Textbox(
                            label=label,
                            placeholder=node["Items"][1]["Value"],
                            interactive=False,
                            elem_id=node["Id"],
                        )

                    output_elements.append(output_obj)
                    elements[node["Id"]] = output_obj

                else:
                    if node["Name"] == "System Prompt":
                        elements[node["Id"]] = gr.Textbox(
                            visible=False, elem_id=node["Id"]
                        )

            normal_edges = [
                edge for edge in request_model["Edges"] if edge["Type"] == "Normal"
            ]
            data_edges = [
                edge for edge in request_model["Edges"] if edge["Type"] == "Data"
            ]

            for edge in normal_edges:
                source_node = request_model["Nodes"][int(edge["Source"]) - 1]
                target_node = request_model["Nodes"][int(edge["Target"]) - 1]

                func = model.get_function(target_node)

                for node in model_schema:
                    if node.idx == int(target_node["Id"]):
                        node.sources.append(int(source_node["Id"]))
                        break
                else:
                    model_schema.append(
                        ModelNode(
                            idx=target_node["Id"],
                            name=request_model["Nodes"][int(edge["Target"]) - 1][
                                "Name"
                            ],
                            sources=[int(source_node["Id"])],
                            func=[func],
                            args=target_node["Items"],
                            overrides=[],
                        )
                    )

            for edge in data_edges:
                source_node = request_model["Nodes"][int(edge["Source"]) - 1]
                source_element = elements[source_node["Id"]]
                target_node = request_model["Nodes"][int(edge["Target"]) - 1]

                override = model.get_override(target_node, edge["Target Handle"])

                for node in model_schema:
                    if node.idx == int(target_node["Id"]):
                        node.overrides.append(
                            {
                                override: (
                                    input_elements.index(source_element) - 1
                                    if chat_interface is None
                                    else input_elements.index(source_element)
                                )
                            }
                        )
                        break
                else:
                    func = model.get_function(target_node)

                    model_schema.append(
                        ModelNode(
                            idx=target_node["Id"],
                            name=request_model["Nodes"][int(edge["Target"]) - 1][
                                "Name"
                            ],
                            sources=[int(source_node["Id"])],
                            func=[func],
                            args=target_node["Items"],
                            overrides=[
                                {
                                    override: (
                                        input_elements.index(source_element) - 1
                                        if chat_interface is None
                                        else input_elements.index(source_element)
                                    )
                                }
                            ],
                        )
                    )

            model.set_model(model_schema)
            model.store_json(request_model)
            logger.info(
                f"API | Update Architecture - Set model: {json.dumps(request_model)}"
            )

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid model architecture provided. Error: {e}",
            )

        model.render_elements(
            chat_interface=chat_interface,
            input_elements=input_elements,
            output_elements=output_elements,
        )

    return Response(status_code=status.HTTP_200_OK)


from .routers import llms, inputs, outputs, chat, helpers

router.include_router(inputs.router, prefix="/inputs", tags=["Input Options"])
router.include_router(chat.router, prefix="/chat", tags=["Chat Options"])
router.include_router(llms.router, prefix="/llms", tags=["LLM Models"])
router.include_router(helpers.router, prefix="/helpers", tags=["Helper Functions"])
router.include_router(outputs.router, prefix="/outputs", tags=["Output Options"])

if "ROSIE" in addons:
    from .routers.addons import rosie
    router.include_router(rosie.router, prefix="/rosie", tags=["ROSIE Options"])
