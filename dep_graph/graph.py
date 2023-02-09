import json
import sys


def get_data(file_name="/tmp/deps.json"):
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"File {file_name} not found.  Aborting")
        sys.exit(1)
    except OSError:
        print(f"OS error occurred trying to open {file_name}")
        sys.exit(1)
    except json.JSONDecodeError as err:
        print(f"JSONDecodeError occurred parsing the {file_name}: {repr(err)}")
        sys.exit(1)
    except Exception as err:
        print(f"Unexpected error opening {file_name} is", repr(err))
        sys.exit(1)

    return data


def dep_resolve(data, node, resolved, unresolved):
    unresolved.append(node)
    print(node)
    for edge in data.get(node):
        if edge not in resolved:
            if edge in unresolved:
                raise Exception(f"Circular reference detected: {node} -> {edge}")
            dep_resolve(data, edge, resolved, unresolved)

    resolved.append(node)
    unresolved.remove(node)


if __name__ == "__main__":
    data = get_data()
    for pkg in data.keys():
        dep_resolve(data, pkg, [], [])
