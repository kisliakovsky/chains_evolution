from typing import List, Set, Iterable

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


def select_favorite_pathway(pathways: List[Pathway]):
    index = len(pathways) // 2
    return pathways[index]


def filter_pathways(pathways: Iterable[Pathway], subpathway: Pathway) -> List[Pathway]:
    return [pathway for pathway in pathways if pathway.startswith(subpathway)]


def filter_pathways_by_clusters(pathways_by_clusters: List[Set[Pathway]], subpathway: Pathway) -> List[Pathway]:
    filtered_pathways_by_clusters = []
    for cluster_pathways in pathways_by_clusters:
        filtered_pathways = filter_pathways(cluster_pathways, subpathway)
        filtered_pathways_by_clusters.append(filtered_pathways)
    return filtered_pathways_by_clusters
