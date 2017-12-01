import json
from typing import Dict, List, Union

from src.distances import calculate_distances


def build_for_cytoscape(sequences: List[str]) -> Union[str, None]:
    return _build_json(sequences)


def _build_json(sequences: List[str]) -> str:
    dictionary = build_as_dict(sequences)
    return json.dumps(dictionary, indent=4)


def build_as_dict(sequences: List[str]) -> Dict:
    distances = calculate_distances(sequences)
    number_of_rows = len(distances)
    number_of_columns = len(distances[0])
    for i in range(1, number_of_rows):
        for j in range(i + 1, number_of_columns):
            print("{} {}: {}".format(i, j, distances[i][j]))
    return {"temp0": distances[0][0], "temp1": distances[1][1]}
