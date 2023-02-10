from typing import Dict, List, NewType

from .utils import get_data


Graph = NewType("Graph", dict)


class CircularDependencyException(Exception):
    "Raised when at least two packages depend on each other"
    pass


class Graph:
    """
    Represents unweighted, directed graph data structure. Implemented using adjacency list

    Attributes:
        graph (Dict, optional): dictionary that holds nodes and edges of the graph
    """

    def __init__(self, json_data: Dict = None) -> None:
        """Constructor for the graph data structure

        Args:
            json_data (Dict, optional): JSON data. Defaults to None.
        """
        self.graph = self._construct_from_json(json_data)

    def _construct_from_json(self, data: Dict) -> Graph:
        """Method that converts the given dictionary to a Graph object

        Args:
            data (Dict): dictionary that holds nodes and edges of a graph

        Returns:
            Graph: newly constructed graph object
        """
        graph = dict()
        if data is None:
            return graph

        for node in data.keys():
            if node not in graph:
                graph[node] = list()
            for edge in data.get(node):
                graph.get(node).append(edge)

        return graph

    def get_nodes(self) -> List[str]:
        """Returns the nodes of the graph

        Returns:
            List[str]: nodes of the graph
        """
        return self.graph.keys()

    def get_edges_for_node(self, node: str) -> List[str]:
        """Returns the edges that are connected to given `node`

        Args:
            node (str): the node to find its edges

        Returns:
            List[str]: the edges that are connected to `node`
        """
        return self.graph.get(node)

    def __str__(self) -> str:
        """Constructs and returns the string representation of the class

        Returns:
            str: string representation of a Graph object
        """
        str = ""
        for node in self.graph.keys():
            str += f"{node} -> {self.graph.get(node)}\n"

        return str


class DependencyGraph:
    """
    Constructs and stores dependency graph of a given graph

    Attributes:
        graph (Graph): a Graph object to construct its dependency graph
        dependency_chains (List[List[str]]) : holds the information of which package depends on which packages

    """

    def __init__(self, graph: Graph) -> None:
        """Constructor for DependencyGraph class

        Args:
            graph (Graph): A Graph object
        """
        self.graph = graph
        self.dependency_chains = list()

    def get_full_dependency_graph(self) -> None:
        """Constructs dependency chains for every node of the graph

        Example:
            Consider this graph: {"a": ["b"], "b": ["c"], "c": ["d", "e"], "d": [], "e": []}.
            This method finds and stores dependencies of every node, namely "a", "b", "c", "d", "e".
            After this method call, dependency_chains attribute looks like this for above graph:
            [
                ["a", "b", "c", "d", "e"],
                ["b", "c", "d", "e"],
                ["c", "d", "e"],
                ["d"],
                ["e"],
            ]
        """
        for node in self.graph.get_nodes():
            chain = self._traverse_dependencies(node, [], [])
            self.dependency_chains.append(chain)

    def _traverse_dependencies(
        self,
        node: str,
        dep_chain: List[str],
        resolved: List[str],
        unresolved: List[str] = [],
    ) -> List[str]:
        """Finds the dependencies of a single node

        Args:
            node (str): node to find its dependencies
            dep_chain (List[str]): holds dependency chain
            resolved (List[str]): holds resolved dependencies
            unresolved (List[str], optional): holds unresolved dependencies. Defaults to [].

        Raises:
            CircularDependencyException: occurs when two or more packages depend on each other

            For instance, a depends b, b depends c and c depends a.

        Returns:
            List[str]: dependency hierarchy
        """
        unresolved.append(node)
        dep_chain.append(node)
        for edge in self.graph.get_edges_for_node(node):
            if edge not in resolved:
                if edge in unresolved:
                    raise CircularDependencyException(
                        f"Circular reference detected: {node} -> {edge}"
                    )
                self._traverse_dependencies(edge, dep_chain, resolved, unresolved)

        resolved.append(node)
        unresolved.remove(node)
        return dep_chain

    def print_dependency_chains(self) -> None:
        """Prints dependency graph (or chains) in human-readable format"""
        for chain in self.dependency_chains:
            str = " - > ".join(chain)
            print(str)


if __name__ == "__main__":
    g = Graph(get_data("/tmp/test.json"))
    dep = DependencyGraph(g)
    dep.get_full_dependency_graph()
    dep.print_dependency_chains()
