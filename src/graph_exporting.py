import json
from pathlib import Path
from typing import List

from src import graph_building
from src import paths

EXPORT_DIR = Path("../export")


def save_for_cytoscape(sequences: List[str], step_name: str):
    section_path = paths.build_section_dir_path(step_name)
    section_path.mkdir(exist_ok=True)
    _save_json(sequences, "forCytoscape", section_path)


def save_for_gephi(sequences: List[str], step_name: str):
    section_path = paths.build_section_dir_path(step_name)
    section_path.mkdir(exist_ok=True)
    _save_csvs(sequences, "forGephi", section_path)


def _save_json(sequences: List[str], file_name: str, section_path: Path):
    dictionary = graph_building.build_as_dict(sequences)
    file_path = paths.build_output_graph_path(section_path, file_name)
    with open(str(file_path), "w") as file:
        json.dump(dictionary, file)


def _save_csvs(sequences: List[str], file_name: str, section_path: Path):
    node_dataframe, edge_dataframe = graph_building.build_as_dataframes(sequences)
    subsection_path = paths.build_subsection_dir_path(section_path, file_name)
    subsection_path.mkdir(exist_ok=True)
    node_file_path = paths.build_output_table_path(subsection_path, "nodes".format(file_name))
    edge_file_path = paths.build_output_table_path(subsection_path, "edges".format(file_name))
    node_dataframe.to_csv(str(node_file_path))
    edge_dataframe.to_csv(str(edge_file_path))
