from typing import Tuple, List, Dict

import pandas
from pandas import DataFrame
# noinspection PyPep8Naming
from numpy import ndarray as NDArray

from src import paths

TRANSITION_MATRIX_FILE_NAME = "Transition_matrix"


def obtain_sources_and_transition_probabilities(index: int, start: str, finish: str) -> Tuple[List[str], Dict[str, NDArray]]:
    file_name = _build_file_name(index)
    dataframe = _load_transition_matrix_file(file_name)
    sources = []
    transition_probabilities_by_sources = {}
    for source, transition_probabilities in dataframe.iterrows():
        source = {
            "_01": start,
            "*01": finish
        }.get(source, source)
        sources.append(source)
        transition_probabilities = transition_probabilities.as_matrix()
        transition_probabilities_by_sources[source] = transition_probabilities
    return sources, transition_probabilities_by_sources


def _load_transition_matrix_file(file_name: str) -> DataFrame:
    file_path = paths.build_input_table_path(file_name)
    return pandas.read_csv(str(file_path), header=0, index_col=0, sep=';')


def _build_file_name(index: int):
    return TRANSITION_MATRIX_FILE_NAME + str(index)
