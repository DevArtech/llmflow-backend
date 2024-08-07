import traceback
import configparser
from fastapi import APIRouter, Response, status, HTTPException

from api.modules.modules import *
from api.modules.handlers import dispatch
from api.modules.graph import GraphApp
from middleware.logging_middleware import logger
from .routers import llms, inputs, outputs, chat, helpers
from api.modules.graph import Graph, GraphNode

addons = []
try:
    config = configparser.ConfigParser()
    config.read("config/config.ini")
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

graph_app = GraphApp(io=gr.Blocks(css=CSS))


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
    if not request_model.get("Nodes") or not request_model.get("Edges"):
        graph_app.render_elements()
        return Response(status_code=status.HTTP_200_OK)
    
    if not graph_app.compare_json(request_model):
        graph = Graph()
        elements = {
            "chat_interface": None,
            "input_elements": [],
            "output_elements": [],
            "data_elements": [],
        }

        for node in request_model["Nodes"]:
            name = node["Name"]
            if "LLM" in node["Name"]:
                name = "LLM"
            handler = dispatch.get(name)
            if handler:
                element = (
                    handler(node)
                    if "Chat" not in name
                    else handler(node, elements["input_elements"], graph_app)
                )
                graph.push(GraphNode(idx=node["Id"], name=node["Name"]))
                if "Chat" in name:
                    elements["chat_interface"] = element
                    elements["input_elements"]
                    elements["output_elements"] = None
                elif "Input" in name:
                    elements["input_elements"].append(element)
                elif "Output" in name:
                    elements["output_elements"].append(element)
                else:
                    elements["data_elements"].append(element)
            else:
                logger.warning(
                    f"API | Update Architecture - No handler for node: {node['Name']}"
                )

        normal_edges = [
            edge for edge in request_model["Edges"] if edge["Type"] == "Normal"
        ]
        data_edges = [
            edge for edge in request_model["Edges"] if edge["Type"] == "Data"
        ]

        for edge in normal_edges:
            source_id = int(edge["Source"])
            target_id = int(edge["Target"])

            target_json = request_model["Nodes"][target_id - 1]
            func = graph_app.get_function(target_json)

            source_node = next((item for item in list(graph.node_index.keys()) if item.idx == source_id), None)
            target_node = next((item for item in list(graph.node_index.keys()) if item.idx == target_id), None)

            target_node.func = [func]
            if graph.node_index[source_node] not in target_node.requires:
                target_node.requires.append(graph.node_index[source_node])
            target_node.args = target_json["Items"]
            graph.connect(source_node, target_node)

        for edge in data_edges:
            source_id = int(edge["Source"])
            target_id = int(edge["Target"])

            target_json = request_model["Nodes"][target_id - 1]
            override = graph_app.get_override(target_json, edge["Target Handle"]) 

            source_node = next((item for item in list(graph.node_index.keys()) if item.idx == source_id), None)
            target_node = next((item for item in list(graph.node_index.keys()) if item.idx == target_id), None)

            if graph.node_index[source_node] not in target_node.requires:
                target_node.requires.append(graph.node_index[source_node])
            if isinstance(target_node.overrides, list):
                target_node.overrides.append(override)
            else:
                target_node.overrides = [override]
            graph.connect(source_node, target_node)

            for k, v in graph.graph.items():
                print("key\n", k, "\n")
                print("value\n", v, "\n")

            graph_app.graph = graph
            graph_app.stored_json = request_model
            logger.info(
                f"API | Update Architecture - Set model: {json.dumps(request_model)}"
            )
        
        if elements["chat_interface"] is None:
            elements["input_elements"].insert(0, gr.Markdown("# Input"))
            elements["output_elements"].insert(0, gr.Markdown("# Output"))

        graph_app.render_elements(
            chat_interface=elements["chat_interface"],
            input_elements=elements["input_elements"],
            output_elements=elements["output_elements"],
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
