from ..graph import Graph, DependencyGraph


class GraphFactory:
    @staticmethod
    def build(data=None):
        return Graph(data)


class DependencyGraphFactory:
    @staticmethod
    def build(graph):
        return DependencyGraph(graph)
