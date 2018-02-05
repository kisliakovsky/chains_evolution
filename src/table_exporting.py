from pandas import DataFrame

from src import paths
from matplotlib import pyplot


def save_table(df: DataFrame, group_idx: int):
    table_path = paths.build_default_output_table_path('group_{}'.format(group_idx))
    df.to_csv(str(table_path))
