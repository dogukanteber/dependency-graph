# dependency-graph
A simple **module** to check package dependencies from a JSON file

### Dependencies

This piece of code uses pure ```Python, v3.10.6```. It also runs with ```Python 3.9``` as well. However, running below ```Python 3.9``` might produce an error due to usage of newly added type hints.

### Test and Run

You may omit 3 from ```python3``` command if you are on Windows.

To run the tests:

```
  python3 -m unittest dep_graph.test.tests -v
```

To run the module:

```
  python3 -m dep_graph.graph
```
