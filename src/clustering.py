from typing import List, Dict

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
        v["new_idx"] = _check_cluster(k, centers)


def _check_cluster(path: str, centers: List[str]) -> List[int]:
    dists = [jellyfish.levenshtein_distance(path, center) for center in centers]
    min_dist = min(dists)
    return [i for i, dist in enumerate(dists) if dist == min_dist]
