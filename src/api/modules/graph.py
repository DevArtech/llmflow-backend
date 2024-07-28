from typing import Dict, List, Union, ClassVar, Callable, Any, Optional
from pydantic import BaseModel


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

    def connect(self, u, v):
        self.push([u, v])
        union = self.uf.union(self.node_index[u], self.node_index[v])
        if union:
            self.graph[u].append(v)
            self.graph[v].append(u)

        return union
