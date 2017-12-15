from typing import List, Dict, Tuple

import jellyfish

from src import distances


def get_cluster_centers(act_matrix: List[List[str]]) -> List[str]:
    centers = []
    for items in act_matrix:
        dist_matrix = distances.calculate_distances(items)
        dists_sums = [sum(row) for row in dist_matrix]
        min_sum = min(dists_sums)
        idx = dists_sums.index(min_sum)
        centers.append(items[idx])
    return centers


def check_clusters(synt_dict: Dict[str, Dict[str, int]], centers: List[str]):
    for k, v in synt_dict.items():
        v["dist"], v["min_dist"], v["new_idx"] = _check_cluster(v["idx"], k, centers)


def check_clusters2(synt_dict: Dict[str, Dict[str, int]], act_mtrx: List[List[str]]):
    for k, v in synt_dict.items():
        v["dist2"], v["min_dist2"], v["new_idx2"] = _check_cluster2(v["idx"], k, act_mtrx)


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
