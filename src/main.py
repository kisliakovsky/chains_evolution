import operator
from typing import List
# noinspection PyPep8Naming
from numpy import ndarray as NDArray

from src.clusters_info import calc_cluster_dist, get_act_path_mtrx, get_cluster_probs
from src.pathways_generating import collect_all_pathways_by_clusters
from src.pathways_processing import remove_repetitive_pathways_by_clusters
from src.pathways_processing import flatten_all_pathways_by_clusters
from src.pathways_processing import select_favorite_pathway
from src.pathways_processing import filter_pathways, count_occurrences_in_clusters, determine_favorite_cluster
from src import graph_exporting, evolution, paths, collects, clustering
from src.evolution import ChildGenerator

import logging

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
    fav_path = "XAFNFIFEFDY"
    act_fav_count, act_path_mtrx = collects.remove_item_from_matrix(fav_path, act_path_mtrx)
    fav_subpaths = evolution.get_evo_subsequences(fav_path)
    cluster_probs = get_cluster_probs()
    for i in range(5):
        print()
        # logger.info("run {}".format(i))
        builder = RunnerBuilder()
        builder.set_idx(i)
        builder.set_act_path_mtrx(act_path_mtrx)
        builder.set_cluster_centers(cluster_centers)
        builder.set_cluster_probs(cluster_probs)
        builder.set_fav_subpaths(fav_subpaths)
        builder.set_act_fav_count(act_fav_count)
        runner = builder.build()
        runner.run()


def obtain_actual_pathways_set():
    actual_pathways_by_clusters = get_act_path_mtrx()
    unique_actual_pathways_by_clusters = remove_repetitive_pathways_by_clusters(actual_pathways_by_clusters)
    return flatten_all_pathways_by_clusters(unique_actual_pathways_by_clusters)


def generate_new_pathways(remained_pathways_set, number):
    new_pathways = []
    if len(remained_pathways_set) != 0:
        pathway_generator = ChildGenerator(remained_pathways_set)
        while (len(new_pathways) + len(remained_pathways_set)) < number:
            new_synthetic_pathway = pathway_generator.generate()
            while new_synthetic_pathway is None:
                new_synthetic_pathway = pathway_generator.generate()
            new_pathways.append(new_synthetic_pathway)
    return new_pathways


if __name__ == '__main__':
    main()
