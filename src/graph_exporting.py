import json
from pathlib import Path
from typing import List, Dict

from src import graph_building
from src import paths


def save_for_cytoscape(sequences: List[str], step_name: str):
    _save_json(sequences, "forCytoscape", step_name)


def save_for_gephi(sequences: Dict[int, List[str]], step_name: str, by_clusters=False):
    _save_csvs(sequences, "forGephi", step_name, by_clusters)


def _save_json(sequences: List[str], file_name: str, step_name: str):
    section_path = paths.create_section(step_name)
    dictionary = graph_building.build_as_dict(sequences, step_name)
    file_path = paths.build_output_graph_path(section_path, file_name)
    with open(str(file_path), "w") as file:
        json.dump(dictionary, file,  indent=4, separators=(',', ': '))


def _save_csvs(sequences: Dict[int, List[str]], file_name: str, step_name: str, by_clusters: bool):
    if by_clusters:
        supersection_path = paths.create_section("byClusters")
    else:
        supersection_path = paths.create_section("flattened")
    section_path = paths.create_subsection(supersection_path, step_name)
    node_dataframe, edge_dataframe = graph_building.build_as_dataframes(sequences)
    subsection_path = paths.create_subsection(section_path, file_name)
    node_file_path = paths.build_output_table_path(subsection_path, "nodes".format(file_name))
    edge_file_path = paths.build_output_table_path(subsection_path, "edges".format(file_name))
    node_dataframe.to_csv(str(node_file_path), index=False)
    edge_dataframe.to_csv(str(edge_file_path), index=False)
