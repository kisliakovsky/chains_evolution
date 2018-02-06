# noinspection PyPep8Naming

import logging

import pandas
from pandas import DataFrame
import seaborn
import numpy
from matplotlib import pyplot

from src import evolution, pathways_processing as process, paths, distances, table_exporting
from src.clusters_info import get_act_path_mtrx, get_cluster_probs
from src.run import RunnerBuilder
from src import chart_exporting

MESSAGE_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# MESSAGE_FORMAT = "%(message)s"
DATE_TIME_FORMAT = "%I:%M:%S %p"

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(fmt=MESSAGE_FORMAT, datefmt=DATE_TIME_FORMAT)
console_handler.setFormatter(formatter)
logger = logging.getLogger('main_logger')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

ACTUAL_PATHWAYS_KEY = "actual"
FAVORITE_PATHWAY_KEY = "favorite"

SYNTHETIC_PATHWAYS_KEY = "synthetic"
# subclasses
REMAINED_PATHWAYS_KEY = "remained"
NEW_PATHWAYS_KEY = "new"
DELETED_PATHWAYS_KEY = "deleted"

Y_BOUND = 15
CURR_CLUSTER = 1


def main():
    act_path_mtrx = get_act_path_mtrx()
    cluster_centers = ['XAFINFEY', 'XAFNIFEFIFEFY', 'XAFIY', 'XAFNIFEDY', 'XAFNIFEY', 'XAFIFEY', 'XAFENIFIFEY']  # squared euclid center
    cluster_centers = process.convert_paths_to_vectors(cluster_centers, act_path_mtrx)
    act_vectors_mtrx = [process.convert_paths_to_vectors(row, act_path_mtrx) for row in act_path_mtrx]
    cluster_lines = []
    for row in act_vectors_mtrx:
        cluster_line = []
        for act_vector in row:
            dist = numpy.sqrt(distances.calculate_default_distance(act_vector['num'], cluster_centers[CURR_CLUSTER]['num']))
            cluster_line.append(dist)
        cluster_lines.append(cluster_line)
    cluster_points = []
    for cluster_center in cluster_centers:
        dist = numpy.sqrt(distances.calculate_default_distance(cluster_center['num'], cluster_centers[CURR_CLUSTER]['num']))
        cluster_points.append([dist])
    # group 0; cluster 0, 2, 5; length 7
    # group 1; cluster 3, 4; length 9
    # group 2; cluster 1, 6; length 12
    # groups = [
    #     {
    #         0: ['XAFEIEY', 'XAFIFDY', 'XAFNFDY'],
    #         2: ['XAFEFDY', 'XAFEIDY', 'XAFIEDY'],
    #         5: ['XAFIFEY', 'XAFNFEY', 'XANIFEY']
    #     },
    #     {
    #         3: ['XAFENIEDY', 'XAFNEFEDY', 'XAFNFEFDY'],
    #         4: ['XAFNFIFEY']
    #     },
    #     {
    #         1: ['XAFNINFNIFEY', 'XAEFIFEFIFDY'],
    #         6: ['XAFNINFIFEDY']
    #     }
    # ]
    groups = [
        {i: [''] for i in range(20)}
    ]
    dfs = []
    for group_idx, group in enumerate(groups):
        statistics = {}
        for fav_index, fav_paths in group.items():
            statistics[fav_index] = {}
            for fav_path_idx, fav_path in enumerate(fav_paths):
                act_path_mtrx = get_act_path_mtrx()
                cluster_probs = get_cluster_probs()
                for i in range(Y_BOUND + 1):
                    statistics[fav_index][i] = []
                successful_runs = 0
                fav_subpaths = None
                while successful_runs < 3:
                    logger.info('')
                    logger.info('Fav index {}'.format(fav_index))
                    logger.info('Run {}'.format(successful_runs))
                    builder = RunnerBuilder()
                    builder.set_idx(successful_runs)
                    builder.set_fav_idx(fav_index)
                    builder.set_act_path_mtrx(act_path_mtrx)
                    builder.set_cluster_centers(cluster_centers)
                    builder.set_cluster_probs(cluster_probs)
                    builder.set_statistics(statistics)
                    builder.set_fav_subpaths(fav_subpaths)
                    runner = builder.build()
                    p, success = runner.run()
                    fav_subpaths = evolution.get_evo_subsequences(p)
                    if success:
                        successful_runs += 1
        steps = []
        fav_indices = []
        runs_or_paths = []
        chances = []
        for fav_idx, values_by_steps in statistics.items():
            for step_idx, values in values_by_steps.items():
                for i, value in enumerate(values):
                    steps.append(step_idx)
                    fav_indices.append(fav_idx)
                    runs_or_paths.append(i + 1)
                    chances.append(value)
        df = DataFrame(data={
            'step': steps,
            'cluster': fav_indices,
            'run': runs_or_paths,
            'distance': chances
        })
        dfs.append(df)
    common_df = pandas.concat(dfs, ignore_index=True)
    table_exporting.save_table(common_df, 0)
    ax = seaborn.tsplot(time='step', value='distance', unit='run', condition='cluster', data=common_df, ci=[95],
                        color='orange', legend=False)
    ax.set_xlim(left=0, right=Y_BOUND + .6)
    ax.set_ylim(bottom=0, top=max([max(cluster_line) for cluster_line in cluster_lines]))
    ax.set_ylabel('distance, symbol')
    ys = cluster_lines[0]
    xs = [Y_BOUND + .05 for y in ys]
    cluster0, = ax.plot(xs, ys, color='blue', linewidth=1.0)
    ax.scatter([Y_BOUND + .05], cluster_points[0], s=20, c='blue')
    ys = cluster_lines[2]
    xs = [Y_BOUND + .15 for y in ys]
    cluster2, = ax.plot(xs, ys, color='green', linewidth=1.0)
    ax.scatter([Y_BOUND + .15], cluster_points[2], s=20, c='green')
    ys = cluster_lines[5]
    xs = [Y_BOUND + .3 for y in ys]
    cluster5, = ax.plot(xs, ys, color='brown', linewidth=1.0)
    ax.scatter([Y_BOUND + .3], cluster_points[5], s=20, c='brown')
    ys = cluster_lines[3]
    xs = [Y_BOUND + .2 for y in ys]
    cluster3, = ax.plot(xs, ys, color='red', linewidth=1.0)
    ax.scatter([Y_BOUND + .2], cluster_points[3], s=20, c='red')
    ys = cluster_lines[4]
    xs = [Y_BOUND + .1 for y in ys]
    cluster4, = ax.plot(xs, ys, color='purple', linewidth=1.0)
    ax.scatter([Y_BOUND + .1], cluster_points[4], s=20, c='purple')
    ys = cluster_lines[1]
    xs = [Y_BOUND for y in ys]
    cluster1, = ax.plot(xs, ys, color='orange', linewidth=1.0)
    ax.scatter([Y_BOUND], cluster_points[1], s=20, c='orange')
    ys = cluster_lines[6]
    xs = [Y_BOUND + .25 for y in ys]
    cluster6, = ax.plot(xs, ys, color='magenta', linewidth=1.0)
    ax.scatter([Y_BOUND + .25], cluster_points[6], s=20, c='magenta')
    pyplot.legend([cluster0, cluster1, cluster2, cluster3, cluster4, cluster5, cluster6],
                  ['cluster 0', 'cluster 1', 'cluster 2', 'cluster 3', 'cluster 4', 'cluster 5', 'cluster 6'],
                  loc='upper center', bbox_to_anchor=(0.5, 1.05),
                  ncol=3, fancybox=True)
    chart_exporting.save_chart(0)


if __name__ == '__main__':
    main()
