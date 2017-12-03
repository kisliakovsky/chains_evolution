import operator

from src.clusters_info import calc_cluster_distribution
from src.pathways import collect_pathways, select_favorite_pathway, filter_pathways
from src import graph_exporting, evolution
from src.evolution import ChildGenerator

import logging

MESSAGE_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_TIME_FORMAT = "%I:%M:%S %p"

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(fmt=MESSAGE_FORMAT, datefmt=DATE_TIME_FORMAT)
console_handler.setFormatter(formatter)
logger = logging.getLogger('main_logger')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


POPULATION_SIZE = 3500


def main():
    population_size = POPULATION_SIZE
    cluster_distribution = calc_cluster_distribution(population_size, random_seed=47)
    cluster_indices, cluster_pathways = collect_pathways(cluster_distribution)
    pathways_set = set(cluster_pathways)
    pathways = list(pathways_set)
    indices = []
    for pathway in pathways:
        index = cluster_pathways.index(pathway)
        cluster_index = cluster_indices[index]
        indices.append(cluster_index)
    pathway_pairs = sorted(zip(indices, pathways), key=operator.itemgetter(0))
    favorite_pathway = select_favorite_pathway(pathways)
    favorite_subpathways = evolution.obtain_evolution_subsequences(favorite_pathway)
    step_name = "main"
    graph_exporting.save_for_gephi({0: pathways}, step_name)
    number_of_steps = len(favorite_subpathways)
    intermediate_step_index = number_of_steps // 2
    last_step_index = number_of_steps - 1
    for step_index, subpathway in enumerate(favorite_subpathways):
        logger.info("Step {}/{}: {}".format(step_index, last_step_index, subpathway))
        filtered_pathways = filter_pathways(pathways, subpathway)
        pathway_generator = ChildGenerator(filtered_pathways)
        new_pathways = filtered_pathways[:]
        while len(new_pathways) < population_size:
            new_pathway = pathway_generator.generate()
            new_pathways.append(new_pathway)
        new_pathways_set = set(new_pathways)
        new_pathways = list(new_pathways_set)
        step_name = "step{}".format(step_index)
        main_pathways = list(pathways_set - new_pathways_set)
        if step_index >= intermediate_step_index:
            graph_exporting.save_for_gephi({0: main_pathways, step_index: new_pathways}, step_name)


if __name__ == '__main__':
    main()
