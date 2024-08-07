import time
import gradio as gr
from typing import Dict, List, Union, ClassVar, Callable, Any, Optional
from pydantic import BaseModel

from api.models.openai import OpenAILLM
from api.models.ollama import OllamaLLM
from langchain_core.messages import SystemMessage
from middleware.logging_middleware import logger


class UnionFind:
    """UnionFind data structure for graph validation"""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1
            return True
        return False


class GraphNode(BaseModel):
    """A node in a list of nodes."""

    idx: int
    name: str
    requires: List[int] = []
    func: List[Callable] = []
    args: List[Dict[str, Any]] = []
    overrides: Optional[List[Dict[str, int]]] = None

    def __hash__(self):
        return hash((self.idx, self.name))



class Graph(BaseModel):
    graph: Dict[GraphNode, GraphNode] = {}
    node_index: Dict[GraphNode, int] = {}
    index: int = 0
    uf: ClassVar = UnionFind(1000)

    def push(self, nodes: Union[GraphNode, List[GraphNode]]) -> None:
        if not isinstance(nodes, list):
            nodes = [nodes]

        for node in nodes:
            if node not in self.node_index:
                self.node_index[node] = self.index
                self.index += 1
                self.graph[node] = []

    def connect(self, u: GraphNode, v: GraphNode):
        self.push([u, v])
        union = self.uf.union(self.node_index[u], self.node_index[v])
        if union:
            self.graph[u].append(v.idx)
            self.graph[v].append(u.idx)

        return union
    

class GraphApp(BaseModel):
    io: Any
    graph: Graph = Graph()
    stored_json: Optional[Dict[str, Any]] = None
    ELEMENTS_PER_ROW: int = 4

    def compare_json(self, json_data: Dict[str, Any]):
        if self.stored_json == None:
            return False

        return self.stored_json == json_data

    def render_elements(
        self,
        chat_interface: Optional[Any] = None,
        input_elements: Optional[List[Any]] = None,
        output_elements: Optional[List[Any]] = None,
    ):
        self.io.clear()

        if input_elements == None:
            input_elements = [
                gr.Markdown(
                    """
                # Welcome to LLMFlow!
                Add some input and output nodes to see the magic happen!
                """
                )
            ]

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
                            for i in range(len(input_elements))[
                                1 :: self.ELEMENTS_PER_ROW
                            ]:
                                with gr.Row():
                                    for element in input_elements[
                                        i : i + self.ELEMENTS_PER_ROW
                                    ]:
                                        element.render()
                            if chat_interface is None:
                                with gr.Row():
                                    btn = gr.Button(
                                        "Submit", size="sm", variant="primary"
                                    )
                                    btn.click(
                                        fn=self.execute_model,
                                        inputs=input_elements[1:],
                                        outputs=output_elements[1:],
                                    )

                    if chat_interface is None:
                        with gr.Column():
                            with gr.Row():
                                if len(output_elements) > 0:
                                    output_elements[0].render()
                            if len(output_elements) > 1:
                                for i in range(len(output_elements))[
                                    1 :: self.ELEMENTS_PER_ROW
                                ]:
                                    with gr.Row():
                                        for element in output_elements[
                                            i : i + self.ELEMENTS_PER_ROW
                                        ]:
                                            element.render()

    def execute_model(self, *args):
        data = args
        for node in self.model:
            for override in node.overrides:
                ovrd_key = list(override.keys())[0]
                ovrd_value = int(override[ovrd_key])
                for dictionary in node.args:
                    if "Type" in dictionary and dictionary["Type"] == ovrd_key:
                        if isinstance(args[0], tuple):
                            dictionary["Value"] = args[0][ovrd_value + 2]
                            logger.info(
                                f"Model | Set {ovrd_key} on node {node.name} to {args[0][ovrd_value + 2]}"
                            )
                        else:
                            dictionary["Value"] = args[ovrd_value]
                            logger.info(
                                f"Model | Set {ovrd_key} on node {node.name} to {args[ovrd_value]}"
                            )

            final_result = []
            for idx, func in enumerate(node.func):
                temp_data = None
                logger.info(f"Model | Executing {func.__name__} on node {node.name}")
                logger.info(f"Model | Input data: {data}")
                logger.info(f"Model | Input args: {node.args}")
                start_time = time.time()
                if isinstance(data, list) or isinstance(data, tuple):
                    try:
                        temp_data = func(data[idx], *node.args)
                    except IndexError:
                        temp_data = func(data[0], *node.args)
                else:
                    temp_data = func(data, *node.args)
                logger.info(
                    f"Model | Finished execution of {func.__name__} on node {node.name} - {time.time() - start_time}s"
                )
                logger.info(f"Model | Function result: {temp_data}")

                final_result.append(temp_data)

            data = final_result
            logger.info(f"Model | Node result: {data}")

        if len(data) == 1:
            return data[0]

        return data

    def execute_chat(self, *args):
        if not self.model:
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

        return (
            str(response[0])
            if isinstance(response, list) or isinstance(response, tuple)
            else str(response)
        )

    def get_function(self, node: Dict[str, Any]):
        if node["Name"] == "System Prompt":

            def function(data, *args):
                return [SystemMessage(content=args[0]["Value"]), data]

        elif node["Name"] == "OpenAI LLM":

            def function(data, *args):
                model = OpenAILLM(
                    api_key=args[0]["Value"],
                    model_type=args[1]["Value"],
                    temperature=float(args[2]["Value"]),
                )
                return model.invoke(data).content

        elif node["Name"] == "Ollama LLM":

            def function(data, *args):
                base_url = (
                    "http://localhost:11434"
                    if args[0]["Value"] == ""
                    else args[0]["Value"]
                )
                system = ""

                if len(data) >= 3 and isinstance(data[2], str):
                    system = data[2]
                else:
                    system = (
                        """You are an assistant developed by the LLMFlow framework. 
                            LLMFlow is a no-code framework that allows anyone to build an LLM application with ease. 
                            They can then take their generated programs to production with code generation and exportation to a Github repository."""
                        if args[3]["Value"] == ""
                        else args[3]["Value"]
                    )
                model = OllamaLLM(
                    base_url=base_url,
                    model_type=args[1]["Value"],
                    temperature=float(args[2]["Value"]),
                    system=system,
                )
                return model.invoke(data)

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

        if node["Name"] == "System Prompt":
            if handle == "element_1":
                return "Prompt"

