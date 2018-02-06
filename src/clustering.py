from typing import List, Dict, Union
import math

import numpy

from src import distances, pathways_processing as process
import logging
logger = logging.getLogger('main_logger')

CURR_CLUSTER = 1


def get_cluster_centers(act_matrix: List[List[str]]) -> List[str]:
    centers = []
    for items in act_matrix:
        dist_matrix = distances.calculate_nastya_distances(items)
        dists_sums = [sum(row) for row in dist_matrix]
        min_sum = min(dists_sums)
        possible_centers = []
        for i, s in enumerate(dists_sums):
            if math.isclose(s, min_sum, rel_tol=1e-5):
                possible_centers.append(items[i])
        centers.append(possible_centers)
    return centers


def determine_cluster(vector: Dict[str, Union[str, List[int]]], centers: List[Dict[str, Union[str, int]]]):
    dists = [distances.calculate_default_distance(vector['num'], center['num']) for center in centers]
    vector_len = len(vector['str'])
    possible_indices = [i for i, dist in enumerate(dists)]
    if vector_len < 4:
        possible_indices = [2]
    elif vector_len == 4:
        possible_indices = [0, 2]
    elif vector_len == 5:
        possible_indices = [0, 2, 6]
    elif vector_len == 6:
        possible_indices = [0, 2, 3, 4, 5, 6]
    elif 6 < vector_len < 9:
        pass
    elif vector_len == 9:
        possible_indices = [0, 1, 2, 3, 4, 6]
    elif 9 < vector_len < 13:
        possible_indices = [0, 1, 3, 4, 6]
    elif vector_len == 13:
        possible_indices = [1, 3, 6]
    elif 13 < vector_len < 17:
        possible_indices = [1, 6]
    elif vector_len >= 17:
        possible_indices = [1]
    possible_dists = [dist for i, dist in enumerate(dists) if i in possible_indices]
    min_dist = min(possible_dists)
    return [possible_indices[i] for i, dist in enumerate(possible_dists) if math.isclose(dist, min_dist, rel_tol=1e-5)]


def calc_dist_to_cluster(vector, center):
    return distances.calculate_default_distance(vector['num'], center['num'])


# def check_clusters2(synt_dict: Dict[str, Dict[str, int]], act_mtrx: List[List[str]]):
#     all_count = 0
#     correct_count = 0
#     incorrect_count = 0
#     error_counts = {
#         0: 0,
#         1: 0,
#         2: 0,
#         3: 0,
#         4: 0,
#         5: 0,
#         6: 0
#     }
#     for k, v in synt_dict.items():
#         v["dist2"], v["min_dist2"], v["new_idx2"] = _check_cluster2(v["idx"], k, act_mtrx)
#         if v["idx"] in v["new_idx2"]:
#             correct_count += v["count"]
#         else:
#             incorrect_count += v["count"]
#             error_counts[v["idx"]] += v["count"]
#         all_count += v["count"]
#     for k in error_counts.keys():
#         error_counts[k] /= incorrect_count
#     return correct_count / all_count, error_counts
#
#
# def _check_cluster2(exp_idx: int, path: str, act_mtrx: List[List[str]]) -> Tuple[int, int, List[int]]:
#     dists = []
#     for items in act_mtrx:
#         dist = min([jellyfish.levenshtein_distance(path, item) for item in items])
#         dists.append(dist)
#     min_dist = min(dists)
#     exp_dist = dists[exp_idx]
#     return exp_dist, min_dist, [i for i, dist in enumerate(dists) if dist == min_dist]


def calc_number_of_paths_by_clusters(synt_paths, cluster_centers):
    counters = [0 for _ in cluster_centers]
    for sp in synt_paths:
        possible_clusters = determine_cluster(sp, cluster_centers)
        for possible_cluster in possible_clusters:
            counters[possible_cluster] += 1 / (len(possible_clusters))
    return counters


def print_pathways_info(synt_paths, cluster_centers, fav_idx):
    number_of_paths = len(synt_paths)
    logger.info('Number of synthetic pathways: {}'.format(len(synt_paths)))
    number_of_paths_by_clusters = calc_number_of_paths_by_clusters(synt_paths, cluster_centers)
    logger.info('Number of synthetic pathways by cluster: {}'.format(str(number_of_paths_by_clusters)))
    chances_of_paths_by_clusters = [count / number_of_paths for count in number_of_paths_by_clusters]
    logger.info('Chances of synthetic pathways by cluster: {}'.format(str(chances_of_paths_by_clusters)))


def print_vertices_info(synt_paths, cluster_centers, fav_idx):
    synt_vertices = set(synt_paths)
    number_of_vertices = len(synt_vertices)
    logger.info('Number of synthetic vertices: {}'.format(number_of_vertices))
    number_of_vertices_by_clusters = calc_number_of_paths_by_clusters(synt_vertices, cluster_centers)
    # logger.info('Number of synthetic vertices by cluster: {}'.format(str(number_of_vertices_by_clusters)))
    chances_of_vertices_by_clusters = [count / number_of_vertices for count in number_of_vertices_by_clusters]
    # maxVal = max(chances_of_vertices_by_clusters)
    # idx = chances_of_vertices_by_clusters.index(maxVal)
    logger.info('Chances of synthetic vertices by cluster: {}'.format(chances_of_vertices_by_clusters[fav_idx]))


def print_quality_info(synt_paths, cluster_centers, fav_idx):
    # print_pathways_info(synt_paths, cluster_centers, fav_idx)
    print_vertices_info(synt_paths, cluster_centers, fav_idx)


def get_chance(synt_paths, act_path_mtrx, cluster_centers, fav_idx):
    synt_vertices = set(synt_paths)
    synt_vectors = process.convert_paths_to_vectors(synt_vertices, act_path_mtrx)
    number_of_vertices = len(synt_vertices)
    logger.info('Number of synthetic vertices: {}'.format(number_of_vertices))
    number_of_vertices_by_clusters = calc_number_of_paths_by_clusters(synt_vectors, cluster_centers)
    chances_of_vertices_by_clusters = [count / number_of_vertices for count in number_of_vertices_by_clusters]
    return chances_of_vertices_by_clusters[fav_idx]


def get_dist(synt_paths, act_path_mtrx, cluster_centers, fav_idx):
    center = cluster_centers[CURR_CLUSTER]  # cluster with shortest paths
    synt_vertices = set(synt_paths)
    synt_vectors = process.convert_paths_to_vectors(synt_vertices, act_path_mtrx)
    number_of_vertices = len(synt_vertices)
    logger.info('Number of synthetic vertices: {}'.format(number_of_vertices))
    return numpy.mean([calc_dist_to_cluster(synt_vector, center) for synt_vector in synt_vectors])
