# noinspection PyPep8Naming

import logging

from src import evolution, collects
from src.clusters_info import get_act_path_mtrx, get_cluster_probs
from src.run import RunnerBuilder

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
    cluster_centers = ['XAFIFDY', 'XAFNIFEFIFEY', 'XAFEY', 'XAFNIFEDY', 'XAFNIFEY', 'XAFIFEY', 'XAFNIFEIFEY']
    fav_paths = ['XAFNFDY', 'XAFNIFEFIFEY', 'XAFDY', 'XAFNFEDY', 'XAFNIFEY', 'XAFIFEY', 'XAFNIFIFEY']
    fav_index = 1
    logger.info('Expected cluster: {}'.format(fav_index))
    fav_path = fav_paths[fav_index]
    act_fav_count, act_path_mtrx = collects.remove_item_from_matrix(fav_path, act_path_mtrx)
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
        builder.set_act_fav_count(act_fav_count)
        runner = builder.build()
        runner.run()


if __name__ == '__main__':
    main()
