import json
from typing import Dict, List, Union, Tuple

from pandas import DataFrame

from src.distances import calculate_distances

Element = Dict[str, Dict[str, str]]


def build_for_cytoscape(sequences: List[str]) -> Union[str, None]:
    return _build_json(sequences)


def _build_json(sequences: List[str]) -> str:
    dictionary = build_as_dict(sequences)
    return json.dumps(dictionary, indent=4)


def build_as_dict(sequences: List[str]) -> List[Element]:
    elements = []
    _add_nodes(elements, sequences)
    distances = calculate_distances(sequences)
    number_of_rows = len(distances)
    number_of_columns = len(distances[0])
    for i in range(1, number_of_rows):
        for j in range(i + 1, number_of_columns):
            weight = int(distances[i][j])
            if weight > 0:
                source = sequences[i]
                target = sequences[j]
                elements.append(_create_edge(source, target, weight))
    return elements


def _add_nodes(elements: List[Element], sequences: List[str]):
    for sequence in sequences:
        elements.append(_create_node(sequence))


def _create_node(identifier: str) -> Element:
    return {
        "data": {"id": identifier}
    }


def _create_edge(source: str, target: str, weight: int) -> Element:
    return {
        "data": {
            "id": source + target,
            "source": source,
            "target": target,
            "weight": weight
        }
    }


def build_as_dataframes(sequences: List[str]) -> Tuple[DataFrame, DataFrame]:
    return DataFrame({'A': []}), DataFrame({'A': []})
