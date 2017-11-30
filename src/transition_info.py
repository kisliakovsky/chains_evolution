import pandas
from pandas import DataFrame
# noinspection PyPep8Naming
from numpy import ndarray as NDArray

from src import paths

TRANSITION_MATRIX_FILE_NAME = "Transition_matrix"


def _load_transition_matrix_file(file_name: str) -> DataFrame:
    file_path = paths.build_input_table_path(file_name)
    return pandas.read_csv(str(file_path), header=0, index_col=0, sep=';')


def _build_file_name(index: int):
    return TRANSITION_MATRIX_FILE_NAME + str(index)


def obtain_transition_matrix(index: int) -> NDArray:
    file_name = _build_file_name(index)
    dataframe = _load_transition_matrix_file(file_name)
    return dataframe.as_matrix()
