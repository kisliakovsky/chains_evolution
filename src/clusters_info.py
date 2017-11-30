from typing import List

import pandas
from pandas import DataFrame, Series
from numpy.random import RandomState

from src import paths

CLUSTER_INFO_FILE_NAME = "clusters_size"
CLUSTER_SIZE_KEY = "CLUSTER_SIZE"


def calc_cluster_distribution(population_size: int, random_seed=47):
    cluster_sizes = _obtain_cluster_sizes(CLUSTER_INFO_FILE_NAME)
    random = RandomState(random_seed)
    return random.multinomial(population_size, cluster_sizes, size=1)[0]


def _obtain_cluster_sizes(file_name: str) -> List[float]:
    dataframe = _load_cluster_sizes_file(file_name)
    cluster_sizes = _obtain_relative_cluster_sizes(dataframe)
    return cluster_sizes.tolist()


def _load_cluster_sizes_file(file_name: str) -> DataFrame:
    file_path = paths.build_input_table_path(file_name)
    return pandas.read_csv(str(file_path), header=0, index_col=0, sep=';')


def _obtain_relative_cluster_sizes(dataframe: DataFrame) -> Series:
    cluster_sizes = _obtain_absolute_cluster_sizes(dataframe)
    cluster_sizes /= cluster_sizes.sum()
    return cluster_sizes


def _obtain_absolute_cluster_sizes(dataframe: DataFrame) -> Series:
    return dataframe[CLUSTER_SIZE_KEY]


# print(calc_cluster_distribution(100))
