from typing import Set

from numpy.random import RandomState

CLUSTER_SIZE = 6
sources = ["Y", "A2", "A1", "B", "X"]
transitions_probs_by_sources = {
    "X": [0, 0, 1, 0, 0],
    "A1": [0.4, 0, 0, 0.6, 0],
    "B": [0.67, 0.33, 0, 0, 0],
    "A2": [1, 0, 0, 0, 0],
    "Y": [0, 0, 0, 0, 0]
}


def _check_all_pathways_is_over(current_sources: Set[str]):
    return len(current_sources) == 1 and list(current_sources)[0] == "Y"


pathways = [["X"] for _ in range(CLUSTER_SIZE)]
current_sources = set(sources[:])
while not _check_all_pathways_is_over(current_sources):
    for source in current_sources:
        if source == "Y":
            continue
        transitions_probs = transitions_probs_by_sources[source]
        selected_pathways = [pathway for pathway in pathways if pathway[-1] == source]
        random = RandomState()
        target_distribution = random.multinomial(len(selected_pathways), transitions_probs, size=1)[0]
        for source_index, target_size in enumerate(target_distribution):
            for _ in range(target_size):
                pathway = selected_pathways.pop()
                pathway.append(sources[source_index])
    current_sources = {pathway[-1] for pathway in pathways}
print(pathways)
