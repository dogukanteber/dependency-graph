from .utils import get_data


class Graph:
    def __init__(self, json_data=None):
        self.graph = self._construct_from_json(json_data)

    def _construct_from_json(self, data):
        graph = dict()
        if data is None:
            return graph

        for node in data.keys():
            if node not in graph:
                graph[node] = list()
            for edge in data.get(node):
                graph.get(node).append(edge)

        return graph

    def get_nodes(self):
        return self.graph.keys()

    def get_edges_for_node(self, node):
        return self.graph.get(node)

    # TODO: prettify the for loop
    def __str__(self):
        str = ""
        for node in self.graph.keys():
            str += f"{node} -> {self.graph.get(node)}\n"

        return str


class DependencyGraph:
    def __init__(self, graph):
        self.graph = graph
        self.dependency_chains = list()

    def get_full_dependency_graph(self):
        for node in self.graph.get_nodes():
            resolved = list()
            chain = self._traverse_dependencies(node, [], resolved)
            self.dependency_chains.append(chain)

    def _traverse_dependencies(self, node, dep_chain, resolved, unresolved=[]):
        unresolved.append(node)
        dep_chain.append(node)
        for edge in self.graph.get_edges_for_node(node):
            if edge not in resolved:
                if edge in unresolved:
                    raise Exception(f"Circular reference detected: {node} -> {edge}")
                self._traverse_dependencies(edge, dep_chain, resolved, unresolved)

        resolved.append(node)
        unresolved.remove(node)
        return dep_chain

    def print_dependency_chains(self):
        for chain in self.dependency_chains:
            str = " - > ".join(chain)
            print(str)


if __name__ == "__main__":
    g = Graph(get_data("/tmp/test.json"))
    dep = DependencyGraph(g)
    dep.get_full_dependency_graph()
    dep.print_dependency_chains()
