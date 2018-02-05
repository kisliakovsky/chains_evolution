from src import paths
from matplotlib import pyplot


def save_chart(group_idx: int):
    chart_path = paths.build_default_output_chart_path('group_{}'.format(group_idx))
    pyplot.savefig(str(chart_path), dpi=200)
