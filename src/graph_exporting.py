import json
from pathlib import Path
from typing import List

from src import graph_building
from src import paths

EXPORT_DIR = Path("../export")


def save_for_cytoscape(sequences: List[str]):
    _save_json(sequences, "forCytoscape")


def save_for_gephi(sequences: List[str]):
    _save_csvs(sequences, "forGephi")


def _save_json(sequences: List[str], file_name: str):
    dictionary = graph_building.build_as_dict(sequences)
    file_path = paths.build_output_graph_path(file_name)
    with open(str(file_path), "w") as file:
        json.dump(dictionary, file)


def _save_csvs(sequences: List[str], file_name: str):
    node_dataframe, edge_dataframe = graph_building.build_as_dataframes(sequences)
    node_file_path = paths.build_output_table_path("{}Nodes".format(file_name))
    edge_file_path = paths.build_output_table_path("{}Edges".format(file_name))
    node_dataframe.to_csv(str(node_file_path))
    edge_dataframe.to_csv(str(edge_file_path))
