import operator

from src.clusters_info import calc_cluster_distribution
from src.pathways_generating import collect_all_pathways_by_clusters
from src.pathways_processing import remove_repetitive_pathways_by_clusters
from src.pathways_processing import flatten_all_pathways_by_clusters
from src.pathways_processing import select_favorite_pathway
from src.pathways_processing import filter_pathways, filter_pathways_by_clusters
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
    number_of_clusters = len(cluster_distribution)
    pathways_by_clusters = collect_all_pathways_by_clusters(cluster_distribution)
    unique_pathways_by_clusters = remove_repetitive_pathways_by_clusters(pathways_by_clusters)
    pathways_set = flatten_all_pathways_by_clusters(unique_pathways_by_clusters)
    pathways = list(pathways_set)
    step_name = "main"
    favorite_pathway = select_favorite_pathway(pathways)
    favorite_pathway_set = {favorite_pathway}
    main_pathways = list(pathways_set - favorite_pathway_set)
    graph_exporting.save_for_gephi({0: main_pathways, 100: [favorite_pathway]}, step_name)
    unique_pathways_by_clusters_dict = {i: cluster_pathways for i, cluster_pathways in enumerate(unique_pathways_by_clusters)}
    # graph_exporting.save_for_gephi(unique_pathways_by_clusters_dict, step_name, by_clusters=True)
    favorite_subpathways = evolution.obtain_evolution_subsequences(favorite_pathway)
    number_of_steps = len(favorite_subpathways)
    intermediate_step_index = number_of_steps // 2
    last_step_index = number_of_steps - 1
    for step_index, subpathway in enumerate(favorite_subpathways):
        logger.info("Step {}/{}: {}".format(step_index, last_step_index, subpathway))
        filtered_pathways = filter_pathways(pathways, subpathway)
        filtered_pathways_by_clusters = filter_pathways_by_clusters(unique_pathways_by_clusters, subpathway)
        occurred_clusters_indices = [i for i, ps in enumerate(filtered_pathways_by_clusters) if len(ps) > 0]
        logger.info("Occurs in clusters: {}".format(str(occurred_clusters_indices)))
        pathway_generator = ChildGenerator(filtered_pathways)
        new_pathways = filtered_pathways[:]
        while len(new_pathways) < population_size:
            new_pathway = pathway_generator.generate()
            while new_pathway is None:
                new_pathway = pathway_generator.generate()
            new_pathways.append(new_pathway)
        new_pathways_set = set(new_pathways)
        new_pathways = list(new_pathways_set)
        step_name = "step{}".format(step_index)
        main_pathways = list((pathways_set - favorite_pathway_set) - new_pathways_set)
        step_pathways = list(new_pathways_set - favorite_pathway_set)
        if step_index >= 0:
            graph_exporting.save_for_gephi({0: main_pathways, step_index: step_pathways, 100: [favorite_pathway]}, step_name)
            export_cluster_dict = {}
            for occurred_clusters_index in occurred_clusters_indices:
                export_cluster_dict[occurred_clusters_index] = list(unique_pathways_by_clusters[occurred_clusters_index] - new_pathways_set)
                export_cluster_dict[number_of_clusters + step_index] = new_pathways
            # graph_exporting.save_for_gephi(export_cluster_dict, step_name, by_clusters=True)



if __name__ == '__main__':
    main()
