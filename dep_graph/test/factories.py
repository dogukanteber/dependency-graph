from ..graph import Graph, DependencyGraph


class GraphFactory:
    @staticmethod
    def build(data: dict = None) -> Graph:
        """Creates a Graph object

        Args:
            data (dict, optional): Graph data as a dictionary. Defaults to None.

        Returns:
            Graph: created Graph object
        """
        return Graph(data)


class DependencyGraphFactory:
    @staticmethod
    def build(graph: Graph) -> DependencyGraph:
        """Creates a DependencyGraph object from the given `Graph`

        Args:
            graph (Graph): Graph object

        Returns:
            DependencyGraph: created DependencyGraph object
        """
        return DependencyGraph(graph)
