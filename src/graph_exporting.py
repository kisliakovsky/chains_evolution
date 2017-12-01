import json
from pathlib import Path
from typing import List

from src import graph_building
from src.paths import build_output_graph_path

EXPORT_DIR = Path("../export")


def save_for_cytoscape(sequences: List[str]):
    _save_json(sequences, "forCytoscape")


def _save_json(sequences: List[str], file_name: str):
    dictionary = graph_building.build_as_dict(sequences)
    file_path = build_output_graph_path(file_name)
    with open(str(file_path), "w") as file:
        json.dump(dictionary, file)
