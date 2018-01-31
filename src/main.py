# noinspection PyPep8Naming

import logging

from src import evolution, collects, clustering
from src.clusters_info import get_act_path_mtrx, get_cluster_probs
from src.run import RunnerBuilder
from src import pathways_processing as process

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

SYNT_PATH_EXPECT_NUM = 100
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
    fav_paths = ['XAFINFEY', 'XAFNIFEFIFEFY', 'XAFIY', 'XAFNIFEDY', 'XAFNIFEY', 'XAFIFEY', 'XAFENIFIFEY']
    # group 0; cluster 0, 2, 5; length 7
    fav_paths = {
        0: ['XAFEIEY', 'XAFIFDY', 'XAFNFDY'],
        2: ['XAFEFDY', 'XAFEIDY', 'XAFIEDY'],
        5: ['XAFIFEY', 'XAFNFEY', 'XANIFEY']
    }
    # group 1; cluster 3, 4; length 9
    # fav_paths = {
    #     3: ['XAFENIEDY', 'XAFNEFEDY', 'XAFNFEFDY'],
    #     4: ['XAFNFIFEY']  # cluster 4
    # }
    # group 2; cluster 1, 6; length 12
    # fav_paths = {
    #     1: ['XAEFIFEFIFDY', 'XAEFIFEFIFEY', 'XAFNIFENEIEY'],
    #     6: ['XAFENEFIFEDY', 'XAFENEIFEIEY', 'XAFNEIFEIFDY']
    # }
    for fav_index, fav_paths in fav_paths.items():
        for fav_path in fav_paths:
            act_path_mtrx = get_act_path_mtrx()
            fav_subpaths = evolution.get_evo_subsequences(fav_path)
            cluster_probs = get_cluster_probs()
            for i in range(10):
                logger.info('')
                logger.info('Run {}'.format(i))
                builder = RunnerBuilder()
                builder.set_idx(i)
                builder.set_fav_idx(fav_index)
                builder.set_act_path_mtrx(act_path_mtrx)
                builder.set_cluster_centers(cluster_centers)
                builder.set_cluster_probs(cluster_probs)
                builder.set_fav_subpaths(fav_subpaths)
                runner = builder.build()
                runner.run()


if __name__ == '__main__':
    main()
