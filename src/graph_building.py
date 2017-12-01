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
    return {"temp0": 55, "temp1": 79}
