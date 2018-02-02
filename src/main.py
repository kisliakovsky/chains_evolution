# noinspection PyPep8Naming

import logging

from pandas import DataFrame
import seaborn

from src import evolution, pathways_processing as process, paths
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


def main():
    act_path_mtrx = get_act_path_mtrx()
    cluster_centers = ['XAFINFEY', 'XAFNIFEFIFEFY', 'XAFIY', 'XAFNIFEDY', 'XAFNIFEY', 'XAFIFEY', 'XAFENIFIFEY'] # squared euclid center
    cluster_centers = process.convert_paths_to_vectors(cluster_centers, act_path_mtrx)
    # group 0; cluster 0, 2, 5; length 7
    # group 1; cluster 3, 4; length 9
    # group 2; cluster 1, 6; length 12
    groups = [
        # {
        #     0: ['XAFEIEY', 'XAFIFDY', 'XAFNFDY'],
        #     2: ['XAFEFDY', 'XAFEIDY', 'XAFIEDY'],
        #     5: ['XAFIFEY', 'XAFNFEY', 'XANIFEY']
        # },
        # {
        #     3: ['XAFENIEDY', 'XAFNEFEDY', 'XAFNFEFDY'],
        #     4: ['XAFNFIFEY']
        # },
        {
            1: ['XAFNINFNIFEY', 'XAEFIFEFIFDY', 'XAFNINFNIFEY'],
            6: ['XAFENFIFEFDY', 'XAFNINFIFEDY', 'XAFENEIFEIEY']
        }
    ]
    for group_idx, group in enumerate(groups):
        statistics = {}
        for fav_index, fav_paths in group.items():
            statistics[fav_index] = {}
            for fav_path_idx, fav_path in enumerate(fav_paths):
                act_path_mtrx = get_act_path_mtrx()
                fav_subpaths = evolution.get_evo_subsequences(fav_path)
                cluster_probs = get_cluster_probs()
                for i, _ in enumerate(fav_subpaths):
                    statistics[fav_index][i] = []
                successful_runs = 0
                while successful_runs < 5:
                    logger.info('')
                    logger.info('Fav index {}'.format(fav_index))
                    logger.info('Fav path index {}'.format(fav_path_idx))
                    logger.info('Fav path {}'.format(fav_path))
                    logger.info('Run {}'.format(successful_runs))
                    builder = RunnerBuilder()
                    builder.set_idx(successful_runs)
                    builder.set_fav_idx(fav_index)
                    builder.set_act_path_mtrx(act_path_mtrx)
                    builder.set_cluster_centers(cluster_centers)
                    builder.set_cluster_probs(cluster_probs)
                    builder.set_fav_subpaths(fav_subpaths)
                    builder.set_statistics(statistics)
                    runner = builder.build()
                    success = runner.run()
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
            'chance': chances
        })
        ax = seaborn.tsplot(time='step', value='chance', unit='run', condition='cluster', data=df, ci=[95])
        chart_exporting.save_chart(group_idx)


if __name__ == '__main__':
    main()
