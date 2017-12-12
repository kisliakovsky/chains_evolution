from typing import List, Set, Iterable
import random

import jellyfish

from src.pathways_generating import Pathway


def remove_repetitive_pathways(all_pathways: List[Pathway]) -> Set[Pathway]:
    return set(all_pathways)


def remove_repetitive_pathways_by_clusters(all_pathways_by_clusters: List[List[Pathway]]) -> List[Set[Pathway]]:
    unique_pathways_by_clusters = []
    for cluster_pathways in all_pathways_by_clusters:
        unique_pathways = remove_repetitive_pathways(cluster_pathways)
        unique_pathways_by_clusters.append(unique_pathways)
    return unique_pathways_by_clusters


def flatten_all_pathways_by_clusters(all_pathways_by_clusters: List[Iterable[Pathway]]) -> Set[Pathway]:
    pathways = set()
    for cluster_pathways in all_pathways_by_clusters:
        for pathway in cluster_pathways:
            pathways.add(pathway)
    return pathways


def select_favorite_pathway(actual_pathways: List[Pathway], synthetic_pathways: List[Pathway]):
    all_min_distances = []
    for synthetic_pathway in synthetic_pathways:
        synthetic_pathway_distances = []
        for actual_pathway in actual_pathways:
            distance = jellyfish.levenshtein_distance(synthetic_pathway, actual_pathway)
            synthetic_pathway_distances.append(distance)
        all_min_distances.append(min(synthetic_pathway_distances))
    index = random.randrange(0, len(all_min_distances))
    return synthetic_pathways[index]


def filter_pathways(pathways: Iterable[Pathway], subpathway: Pathway, is_last: bool) -> Set[Pathway]:
    return {pathway for pathway in pathways if pathway.startswith(subpathway) and ((not is_last) or (len(pathway) <= len(subpathway)))}


def filter_pathways_by_clusters(pathways_by_clusters: List[Set[Pathway]], subpathway: Pathway) -> List[Pathway]:
    filtered_pathways_by_clusters = []
    for cluster_pathways in pathways_by_clusters:
        filtered_pathways = filter_pathways(cluster_pathways, subpathway)
        filtered_pathways_by_clusters.append(filtered_pathways)
    return filtered_pathways_by_clusters
