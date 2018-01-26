from typing import List, Dict, Tuple

import jellyfish

from src import distances
import logging
logger = logging.getLogger('main_logger')


def get_cluster_centers(act_matrix: List[List[str]]) -> List[str]:
    centers = []
    for items in act_matrix:
        dist_matrix = distances.calculate_nastya_distances(items)
        dists_sums = [sum(row) for row in dist_matrix]
        min_sum = min(dists_sums)
        possible_centers = []
        for i, s in enumerate(dists_sums):
            if s == min_sum:
                possible_centers.append(items[i])
        centers.append(possible_centers)
    return centers


def determine_cluster(path: str, centers: List[str]):
    dists = [distances.calculate_distance(path, center) for center in centers]
    min_dist = min(dists)
    return [i for i, dist in enumerate(dists) if dist == min_dist]


def check_clusters(synt_dict: Dict[str, Dict[str, int]], centers: List[str]):
    all_count = 0
    correct_count = 0
    incorrect_count = 0
    error_counts = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }
    for k, v in synt_dict.items():
        v["dist"], v["min_dist"], v["new_idx"] = _check_cluster(v["idx"], k, centers)
        if v["idx"] in v["new_idx"]:
            correct_count += v["count"]
        else:
            incorrect_count += v["count"]
            error_counts[v["idx"]] += v["count"]
        all_count += v["count"]
    for k in error_counts.keys():
        error_counts[k] /= incorrect_count
    return correct_count / all_count, error_counts


def check_clusters2(synt_dict: Dict[str, Dict[str, int]], act_mtrx: List[List[str]]):
    all_count = 0
    correct_count = 0
    incorrect_count = 0
    error_counts = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0
    }
    for k, v in synt_dict.items():
        v["dist2"], v["min_dist2"], v["new_idx2"] = _check_cluster2(v["idx"], k, act_mtrx)
        if v["idx"] in v["new_idx2"]:
            correct_count += v["count"]
        else:
            incorrect_count += v["count"]
            error_counts[v["idx"]] += v["count"]
        all_count += v["count"]
    for k in error_counts.keys():
        error_counts[k] /= incorrect_count
    return correct_count / all_count, error_counts


def _check_cluster(exp_idx: int, path: str, centers: List[str]) -> Tuple[int, int, List[int]]:
    dists = [jellyfish.levenshtein_distance(path, center) for center in centers]
    min_dist = min(dists)
    exp_dist = dists[exp_idx]
    return exp_dist, min_dist, [i for i, dist in enumerate(dists) if dist == min_dist]


def _check_cluster2(exp_idx: int, path: str, act_mtrx: List[List[str]]) -> Tuple[int, int, List[int]]:
    dists = []
    for items in act_mtrx:
        dist = min([jellyfish.levenshtein_distance(path, item) for item in items])
        dists.append(dist)
    min_dist = min(dists)
    exp_dist = dists[exp_idx]
    return exp_dist, min_dist, [i for i, dist in enumerate(dists) if dist == min_dist]


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


def get_chance(synt_paths, cluster_centers, fav_idx):
    synt_vertices = set(synt_paths)
    number_of_vertices = len(synt_vertices)
    logger.info('Number of synthetic vertices: {}'.format(number_of_vertices))
    number_of_vertices_by_clusters = calc_number_of_paths_by_clusters(synt_vertices, cluster_centers)
    chances_of_vertices_by_clusters = [count / number_of_vertices for count in number_of_vertices_by_clusters]
    return chances_of_vertices_by_clusters[fav_idx]

