from typing import List, Dict

from src import graph_building
from src import paths


def save_for_gephi(sequences: Dict[str, List[str]], fav_node_length: int, run_index: int, step_name: str):
    _save_csvs(sequences, fav_node_length, run_index, step_name)


def save_log(message: str, fav_node_length: int, run_index: int):
    main_path = paths.create_section("length{}".format(fav_node_length))
    section_path = paths.create_subsection(main_path, "run{}".format(run_index))
    log_file_path = paths.build_output_log_path(section_path, "log")
    with open(str(log_file_path), 'a') as log_file:
        log_file.write(message + "\n")


def save_csv_log_title(row: List[str], fav_node_length: int, run_index: int):
    main_path = paths.create_section("length{}".format(fav_node_length))
    log_file_path = paths.build_output_table_path(main_path, "run{}".format(run_index))
    with open(str(log_file_path), 'a') as log_file:
        log_file.write(",".join(row) + "\n")


def save_csv_log(row: List[int], fav_node_length: int, run_index: int):
    main_path = paths.create_section("length{}".format(fav_node_length))
    log_file_path = paths.build_output_table_path(main_path, "run{}".format(run_index))
    row = [str(item) for item in row]
    with open(str(log_file_path), 'a') as log_file:
        log_file.write(",".join(row) + "\n")


def _save_csvs(sequences: Dict[str, List[str]], fav_node_length: int, run_index: int, step_name: str):
    main_path = paths.create_section("length{}".format(fav_node_length))
    supersection_path = paths.create_subsection(main_path, "run{}".format(run_index))
    section_path = paths.create_subsection(supersection_path, step_name)
    node_dataframe, edge_dataframe = graph_building.build_as_dataframes(sequences)
    node_file_path = paths.build_output_table_path(section_path, "nodes")
    edge_file_path = paths.build_output_table_path(section_path, "edges")
    node_dataframe.to_csv(str(node_file_path), index=False)
    edge_dataframe.to_csv(str(edge_file_path), index=False)
