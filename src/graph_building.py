import json
from typing import Dict, List, Union, Tuple, Callable

from pandas import DataFrame

from src.distances import calculate_distances

Element = Dict[str, Dict[str, str]]
MAX_EDGE_WEIGHT = 3


def build_for_cytoscape(sequences: List[str], step_name: str) -> Union[str, None]:
    return _build_json(sequences, step_name)


def _build_json(sequences: List[str], step_name: str) -> str:
    dictionary = build_as_dict(sequences, step_name)
    return json.dumps(dictionary, indent=4, separators=(',', ': '))


def build_as_dict(sequences: List[str], step_name: str) -> List[Element]:
    elements = []
    _add_nodes(elements, sequences, step_name)

    def handler(source: str, target: str, weight: int):
        elements.append(_create_edge(source, target, weight))
    _map_edge_components(sequences, handler)
    return elements


def _add_nodes(elements: List[Element], sequences: List[str], step_name: str):
    for sequence in sequences:
        elements.append(_create_node(sequence, step_name))


def _create_node(identifier: str, step_name: str) -> Element:
    return {
        "data": {"id": identifier}
    }


def _create_edge(source: str, target: str, weight: int) -> Element:
    return {
        "data": {
            "id": "{}_{}".format(source,target),
            "source": source,
            "target": target,
            "weight": weight
        }
    }


def build_as_dataframes(sequences: List[str], step_name: str) -> Tuple[DataFrame, DataFrame]:
    nodes = _create_node_dataframe(sequences, step_name)
    edges = _create_edge_dataframe(sequences, step_name)
    return nodes, edges


def _create_node_dataframe(sequences: List[str], step_name: str):
    nodes = {
        "Id": sequences,
        "Label": sequences,
        "Class": [step_name for _ in sequences]
    }
    return DataFrame(data=nodes)


def _create_edge_dataframe(sequences: List[str], step_name: str):
    sources = []
    targets = []
    types = []
    ids = []
    weights = []

    def handler(source: str, target: str, weight: str):
        sources.append(source)
        targets.append(target)
        types.append("Undirected")
        ids.append("{}_{}".format(source, target))
        weights.append(weight)

    # PyCharm bug
    # noinspection PyTypeChecker
    _map_edge_components(sequences, handler)
    edges = {
        "Source": sources,
        "Target": targets,
        "Type": types,
        "Id": ids,
        "Label": weights,
        "Weight": weights,
        "Class": step_name
    }
    return DataFrame(data=edges)


def _map_edge_components(sequences: List[str], handler: Callable[[str, str, int], None]):
    distances = calculate_distances(sequences)
    number_of_rows = len(distances)
    number_of_columns = len(distances[0])
    for i in range(1, number_of_rows):
        for j in range(i + 1, number_of_columns):
            weight = int(distances[i][j])
            if 0 < weight < MAX_EDGE_WEIGHT:
                source = sequences[i]
                target = sequences[j]
                handler(source, target, weight)
