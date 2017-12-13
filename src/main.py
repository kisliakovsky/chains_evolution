import operator

from src.clusters_info import calc_cluster_distribution, obtain_actual_pathways_by_clusters
from src.pathways_generating import collect_all_pathways_by_clusters
from src.pathways_processing import remove_repetitive_pathways_by_clusters
from src.pathways_processing import flatten_all_pathways_by_clusters
from src.pathways_processing import select_favorite_pathway
from src.pathways_processing import filter_pathways, count_occurrences_in_clusters, determine_favorite_cluster
from src import graph_exporting, evolution, paths
from src.evolution import ChildGenerator

import logging

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

EXPECTED_NUMBER_OF_SYNTHETIC_PATHWAYS = 100
START_POPULATION_SIZE = 939
ACTUAL_PATHWAYS_KEY = "actual"
FAVORITE_PATHWAY_KEY = "favorite"

SYNTHETIC_PATHWAYS_KEY = "synthetic"
# subclasses
REMAINED_PATHWAYS_KEY = "remained"
NEW_PATHWAYS_KEY = "new"
DELETED_PATHWAYS_KEY = "deleted"


def main():
    for i in range(1000):
        logger.info("run {}".format(i))
        run(i)


def run(run_index: int):
    actual_pathways_by_clusters = obtain_actual_pathways_by_clusters()
    unique_actual_pathways_by_clusters = remove_repetitive_pathways_by_clusters(actual_pathways_by_clusters)
    actual_pathways_set = flatten_all_pathways_by_clusters(unique_actual_pathways_by_clusters)
    actual_pathways = list(actual_pathways_set)
    # graph_exporting.save_for_kirill({ACTUAL_PATHWAYS_KEY: actual_pathways}, "actual_data_graph")
    synthetic_pathways_set = obtain_synthetic_pathways_set()
    synthetic_pathways = list(synthetic_pathways_set)
    favorite_pathway = select_favorite_pathway(actual_pathways, synthetic_pathways)
    favorite_pathway_set = {favorite_pathway}
    actual_pathways_but_favorite = list(actual_pathways_set - favorite_pathway_set)
    synthetic_pathways_but_actual_and_favorite = list(
        synthetic_pathways_set - actual_pathways_set - favorite_pathway_set)
    favorite_pathway_length = len(favorite_pathway)
    graph_exporting.save_csv_log_title(["cluster{}".format(ci) for ci, _ in enumerate(unique_actual_pathways_by_clusters)], favorite_pathway_length, run_index)
    favorite_subpathways = evolution.obtain_evolution_subsequences(favorite_pathway)
    number_of_steps = len(favorite_subpathways)
    last_step_index = number_of_steps - 1
    for step_index, subpathway in enumerate(favorite_subpathways):
        remained_pathways_set = filter_pathways(synthetic_pathways, subpathway, last_step_index == step_index)
        remained_pathways = list(remained_pathways_set)
        deleted_pathways_set = synthetic_pathways_set - remained_pathways_set
        deleted_pathways = list(deleted_pathways_set)
        new_pathways_set = set(generate_new_pathways(remained_pathways_set, len(synthetic_pathways_set)))
        new_pathways = list(new_pathways_set)
        remained_pathways_but_actual_and_favorite = list(remained_pathways_set - actual_pathways_set - favorite_pathway_set)
        new_pathways_but_actual_and_remained_and_favorite = list(new_pathways_set - actual_pathways_set - remained_pathways_set - favorite_pathway_set)
        deleted_pathways_but_actual = list(deleted_pathways_set - actual_pathways_set)
        step_name = "synthetic_data_after_step{}".format(step_index)
        synthetic_pathways_set = remained_pathways_set | new_pathways_set
        synthetic_pathways = list(synthetic_pathways_set)
        synthetic_occurrences = count_occurrences_in_clusters(synthetic_pathways + [favorite_pathway], unique_actual_pathways_by_clusters)
        if last_step_index != step_index:
            graph_exporting.save_csv_log(synthetic_occurrences, favorite_pathway_length, run_index)
    favorite_pathway_cluster = determine_favorite_cluster(favorite_pathway, unique_actual_pathways_by_clusters)
    graph_exporting.save_csv_log(favorite_pathway_cluster, favorite_pathway_length, run_index)


def obtain_actual_pathways_set():
    actual_pathways_by_clusters = obtain_actual_pathways_by_clusters()
    unique_actual_pathways_by_clusters = remove_repetitive_pathways_by_clusters(actual_pathways_by_clusters)
    return flatten_all_pathways_by_clusters(unique_actual_pathways_by_clusters)


def obtain_synthetic_pathways_set():
    population_size = START_POPULATION_SIZE
    synthetic_pathways_set = {}
    actual_number_of_synthetic_pathways = len(synthetic_pathways_set)
    while actual_number_of_synthetic_pathways < EXPECTED_NUMBER_OF_SYNTHETIC_PATHWAYS:
        cluster_distribution = calc_cluster_distribution(population_size, random_seed=47)
        synthetic_pathways_by_clusters = collect_all_pathways_by_clusters(cluster_distribution)
        unique_synthetic_pathways_by_clusters = remove_repetitive_pathways_by_clusters(synthetic_pathways_by_clusters)
        synthetic_pathways_set = flatten_all_pathways_by_clusters(unique_synthetic_pathways_by_clusters)
        actual_number_of_synthetic_pathways = len(synthetic_pathways_set)
        population_size += 1
    return synthetic_pathways_set


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
