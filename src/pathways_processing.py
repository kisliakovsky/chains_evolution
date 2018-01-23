from typing import List, Set, Iterable, Tuple
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


def flatten_all_pathways_by_clusters(all_pathways_by_clusters: List[List[Pathway]]) -> List[Pathway]:
    pathways = []
    for cluster_pathways in all_pathways_by_clusters:
        for pathway in cluster_pathways:
            pathways.append(pathway)
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


def filter_pathways(pathways: Iterable[Pathway], subpathway: Pathway, is_last: bool) -> Tuple[List[Pathway], List[Pathway]]:
    remained, deleted = [], []
    for pathway in pathways:
        if pathway.startswith(subpathway) and ((not is_last) or (len(pathway) <= len(subpathway))):
            remained.append(pathway)
        else:
            deleted.append(pathway)
    return remained, deleted


def count_occurrences_in_clusters(synthetic_pathways: List[Pathway], actual_pathways_by_clusters: Iterable[Iterable[Pathway]]) -> List[int]:
    counts = [0 for _ in actual_pathways_by_clusters]
    for synthetic_pathway in synthetic_pathways:
        indices = _determine_clusters(synthetic_pathway, actual_pathways_by_clusters)
        for index in indices:
            counts[index] += 1
    return counts


def determine_favorite_cluster(favorite_pathway: Pathway, actual_pathways_by_clusters: Iterable[Iterable[Pathway]]) -> List[int]:
    counts = [0 for _ in actual_pathways_by_clusters]
    indices = _determine_clusters(favorite_pathway, actual_pathways_by_clusters)
    for index in indices:
        counts[index] = 1
    return counts


def _determine_clusters(pathway: Pathway, actual_pathways_by_clusters: Iterable[Iterable[Pathway]]) -> List[int]:
    distances = [0 for _ in actual_pathways_by_clusters]
    for i, actual_pathways in enumerate(actual_pathways_by_clusters):
        for actual_pathway in actual_pathways:
            distance = jellyfish.levenshtein_distance(pathway, actual_pathway)
            distances[i] += distance
        distances[i] /= len(actual_pathways)
    smallest = min(distances)
    indices = [index for index, element in enumerate(distances) if smallest == element]
    return indices


def filter_pathways_by_clusters(pathways_by_clusters: List[List[Pathway]], subpathway: Pathway, is_last: bool) -> Tuple[List[List[Pathway]], List[List[Pathway]]]:
    remained_pathways_by_clusters = []
    deleted_pathways_by_clusters = []
    for cluster_pathways in pathways_by_clusters:
        remained, deleted = filter_pathways(cluster_pathways, subpathway, is_last)
        remained_pathways_by_clusters.append(remained)
        deleted_pathways_by_clusters.append(deleted)
    return remained_pathways_by_clusters, deleted_pathways_by_clusters
