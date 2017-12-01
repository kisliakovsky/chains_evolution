from typing import Set, List

from numpy.random import RandomState
# noinspection PyPep8Naming
from numpy import ndarray as NDArray


from src.transition_info import obtain_sources_and_transition_probabilities

START_LOCATION = "X"
FINISH_LOCATION = "Y"


def collect_unique_pathways(cluster_distribution: NDArray) -> List[str]:
    pathways = collect_pathways(cluster_distribution)
    return list(set(pathways))


def collect_pathways(cluster_distribution: NDArray) -> List[str]:
    pathways_by_clusters = collect_pathways_by_clusters(cluster_distribution)
    return [pathway for cluster_pathways in pathways_by_clusters for pathway in cluster_pathways]


def collect_pathways_by_clusters(cluster_distribution: NDArray) -> List[List[str]]:
    pathways_by_clusters = _collect_pathways_by_clusters(cluster_distribution)
    new_pathways_by_clusters = []
    for pathways in pathways_by_clusters:
        new_pathways = []
        for pathway in pathways:
            new_pathway = ''.join((location[0] for location in pathway))
            new_pathways.append(new_pathway)
        new_pathways_by_clusters.append(new_pathways)
    return new_pathways_by_clusters


def _collect_pathways_by_clusters(cluster_distribution: NDArray) -> List[List[List[str]]]:
    pathways_by_clusters = []
    for i, cluster_size in enumerate(cluster_distribution):
        sources, transition_probabilities_by_sources = obtain_sources_and_transition_probabilities(i, START_LOCATION,
                                                                                                   FINISH_LOCATION)
        cluster_pathways = [[START_LOCATION] for _ in range(cluster_size)]
        current_sources = set(sources[:])
        while not _check_all_pathways_is_over(current_sources):
            for source in current_sources:
                if source == FINISH_LOCATION:
                    continue
                transitions_probs = transition_probabilities_by_sources[source]
                selected_pathways = [pathway for pathway in cluster_pathways if pathway[-1] == source]
                random = RandomState()
                target_distribution = random.multinomial(len(selected_pathways), transitions_probs, size=1)[0]
                for source_index, target_size in enumerate(target_distribution):
                    for _ in range(target_size):
                        pathway = selected_pathways.pop()
                        pathway.append(sources[source_index])
            current_sources = {pathway[-1] for pathway in cluster_pathways}
        pathways_by_clusters.append(cluster_pathways)
    return pathways_by_clusters


def _check_all_pathways_is_over(current_sources: Set[str]):
    return len(current_sources) == 1 and list(current_sources)[0] == FINISH_LOCATION
