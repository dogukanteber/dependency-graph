import unittest
from dataclasses import dataclass

from ..graph import CircularDependencyException
from .factories import GraphFactory, DependencyGraphFactory


@dataclass
class FullDependencyTestCase:
    """Data class to represent a dependency test case

    It is created to write table-driven test cases.
    """

    input: list[str]
    expected: list[str]


@dataclass
class SingleDependencyTestCase(FullDependencyTestCase):
    """Data class to represent a single test case of `FullDependencyTestCase`

    It is created to write table-driven test cases.
    """

    node: str


class TestDependencyGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.test_cases = [
            FullDependencyTestCase(
                input={"a": ["b"], "b": ["c"], "c": ["d", "e"], "d": [], "e": []},
                expected=[
                    ["a", "b", "c", "d", "e"],
                    ["b", "c", "d", "e"],
                    ["c", "d", "e"],
                    ["d"],
                    ["e"],
                ],
            ),
            FullDependencyTestCase(
                input={"a": [], "b": [], "c": [], "d": []},
                expected=[["a"], ["b"], ["c"], ["d"]],
            ),
            FullDependencyTestCase(
                input={
                    "a": ["b", "f"],
                    "b": ["c", "d", "e"],
                    "c": [],
                    "d": ["e"],
                    "e": ["g"],
                    "f": ["b"],
                    "g": [],
                },
                expected=[
                    ["a", "b", "c", "d", "e", "g", "f"],
                    ["b", "c", "d", "e", "g"],
                    ["c"],
                    ["d", "e", "g"],
                    ["e", "g"],
                    ["f", "b", "c", "d", "e", "g"],
                    ["g"],
                ],
            ),
            FullDependencyTestCase(
                input={
                    "a": [],
                    "b": [],
                    "c": [],
                },
                expected=[
                    ["a"],
                    ["b"],
                    ["c"],
                ],
            ),
        ]

        # The reason why this list is 2D is to remove the unnecessary creations
        # of Graph and DependencyGraph objects.
        self.single_test_cases = [
            [
                SingleDependencyTestCase(
                    node="a",
                    input={"a": ["b"], "b": ["c"], "c": ["d", "e"], "d": [], "e": []},
                    expected=["a", "b", "c", "d", "e"],
                ),
                SingleDependencyTestCase(
                    node="b",
                    input={"a": ["b"], "b": ["c"], "c": ["d", "e"], "d": [], "e": []},
                    expected=["b", "c", "d", "e"],
                ),
                SingleDependencyTestCase(
                    node="c",
                    input={"a": ["b"], "b": ["c"], "c": ["d", "e"], "d": [], "e": []},
                    expected=["c", "d", "e"],
                ),
                SingleDependencyTestCase(
                    node="d",
                    input={"a": ["b"], "b": ["c"], "c": ["d", "e"], "d": [], "e": []},
                    expected=["d"],
                ),
                SingleDependencyTestCase(
                    node="e",
                    input={"a": ["b"], "b": ["c"], "c": ["d", "e"], "d": [], "e": []},
                    expected=["e"],
                ),
            ],
            [
                SingleDependencyTestCase(
                    node="a", input={"a": [], "b": [], "c": [], "d": []}, expected=["a"]
                ),
                SingleDependencyTestCase(
                    node="b", input={"a": [], "b": [], "c": [], "d": []}, expected=["b"]
                ),
                SingleDependencyTestCase(
                    node="c", input={"a": [], "b": [], "c": [], "d": []}, expected=["c"]
                ),
                SingleDependencyTestCase(
                    node="d", input={"a": [], "b": [], "c": [], "d": []}, expected=["d"]
                ),
            ],
            [
                SingleDependencyTestCase(
                    node="a",
                    input={
                        "a": ["b", "f"],
                        "b": ["c", "d", "e"],
                        "c": [],
                        "d": ["e"],
                        "e": ["g"],
                        "f": ["b"],
                        "g": [],
                    },
                    expected=["a", "b", "c", "d", "e", "g", "f"],
                ),
                SingleDependencyTestCase(
                    node="b",
                    input={
                        "a": ["b", "f"],
                        "b": ["c", "d", "e"],
                        "c": [],
                        "d": ["e"],
                        "e": ["g"],
                        "f": ["b"],
                        "g": [],
                    },
                    expected=["b", "c", "d", "e", "g"],
                ),
                SingleDependencyTestCase(
                    node="c",
                    input={
                        "a": ["b", "f"],
                        "b": ["c", "d", "e"],
                        "c": [],
                        "d": ["e"],
                        "e": ["g"],
                        "f": ["b"],
                        "g": [],
                    },
                    expected=["c"],
                ),
                SingleDependencyTestCase(
                    node="d",
                    input={
                        "a": ["b", "f"],
                        "b": ["c", "d", "e"],
                        "c": [],
                        "d": ["e"],
                        "e": ["g"],
                        "f": ["b"],
                        "g": [],
                    },
                    expected=["d", "e", "g"],
                ),
                SingleDependencyTestCase(
                    node="e",
                    input={
                        "a": ["b", "f"],
                        "b": ["c", "d", "e"],
                        "c": [],
                        "d": ["e"],
                        "e": ["g"],
                        "f": ["b"],
                        "g": [],
                    },
                    expected=["e", "g"],
                ),
                SingleDependencyTestCase(
                    node="f",
                    input={
                        "a": ["b", "f"],
                        "b": ["c", "d", "e"],
                        "c": [],
                        "d": ["e"],
                        "e": ["g"],
                        "f": ["b"],
                        "g": [],
                    },
                    expected=["f", "b", "c", "d", "e", "g"],
                ),
                SingleDependencyTestCase(
                    node="g",
                    input={
                        "a": ["b", "f"],
                        "b": ["c", "d", "e"],
                        "c": [],
                        "d": ["e"],
                        "e": ["g"],
                        "f": ["b"],
                        "g": [],
                    },
                    expected=["g"],
                ),
            ],
        ]

        self.circular_dependency_cases = [
            [
                SingleDependencyTestCase(
                    node="a", input={"a": ["b"], "b": ["a"]}, expected={}
                ),
                SingleDependencyTestCase(
                    node="b", input={"a": ["b"], "b": ["a"]}, expected={}
                ),
            ]
        ]

    def test_get_full_dependency_graph(self):
        for case in self.test_cases:
            dep_graph = DependencyGraphFactory.build(GraphFactory.build(case.input))
            dep_graph.get_full_dependency_graph()
            actual = dep_graph.dependency_chains
            self.assertListEqual(
                case.expected,
                actual,
                f"failed test! expected {case.expected}, actual {actual}",
            )

    def test_traverse_dependencies(self):
        for i, graph in enumerate(self.single_test_cases):
            dep_graph = DependencyGraphFactory.build(GraphFactory.build(graph[i].input))
            for case in graph:
                actual = dep_graph._traverse_dependencies(case.node, [], [])
                self.assertListEqual(
                    case.expected,
                    actual,
                    f"failed test! expected {case.expected}, actual {actual}",
                )

    def test_traverse_dependencies_circular(self):
        for i, graph in enumerate(self.circular_dependency_cases):
            dep_graph = DependencyGraphFactory.build(GraphFactory.build(graph[i].input))
            for case in graph:
                with self.assertRaises(CircularDependencyException):
                    dep_graph._traverse_dependencies(case.node, [], [])
