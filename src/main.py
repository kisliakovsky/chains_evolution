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
    fav_paths = ['XAFNINFIFEDY', 'XAFNINFEIFEY', 'XAFENFIFEFDY', 'XANINFNIFEFY', 'XAFNFIFEFIEY', 'XAFNINFENFEY']
    for fav_path in fav_paths:
        fav_vector = process.convert_path_to_vector(fav_path, process.flatten_all_pathways_by_clusters(act_path_mtrx))
        res = clustering.determine_cluster(fav_vector, cluster_centers)
        print(res)


if __name__ == '__main__':
    main()
