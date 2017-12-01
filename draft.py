from numpy.random import RandomState

CLUSTER_SIZE = 6
sources = ["X", "A1", "B", "A2", "Y"]
transitions_probs_by_sources = {
    "X": [0, 1, 0, 0, 0],
    "A1": [0, 0, 0.6, 0, 0.4],
    "B": [0, 0, 0, 0.33, 0.67],
    "A2": [0, 0, 0, 0, 1],
    "Y": [0, 0, 0, 0, 0]
}
pathways = [["X"] for _ in range(CLUSTER_SIZE)]
for source in sources:
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
print(pathways)
