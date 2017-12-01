from numpy.random import RandomState

from src.clusters_info import calc_cluster_distribution
from src.transition_info import obtain_sources_and_transition_probabilities

NUMBER_OF_CLUSTERS = 10
POPULATION_SIZE = 100

CACHE = True
CACHED_CLUSTER_DISTRIBUTION = [1, 34, 14, 4, 19, 8, 2, 6, 6, 6]


def main():
    if CACHE:
        cluster_distribution = CACHED_CLUSTER_DISTRIBUTION
    else:
        cluster_distribution = calc_cluster_distribution(POPULATION_SIZE, random_seed=47)
    for i in range(NUMBER_OF_CLUSTERS):
        cluster_size = cluster_distribution[i]
        sources, transition_probabilities_by_sources = obtain_sources_and_transition_probabilities(i)
        pathway_counter = 0
        pathways = []
        for _ in range(cluster_size):
            pathways.append(["X"])
        while pathway_counter < cluster_size:
            pathway = pathways[pathway_counter]
            next_source = pathway[-1]
            if next_source == "Y":
                pathway_counter += 1
                continue
            else:
                transition_probabilities = transition_probabilities_by_sources[next_source]
                random = RandomState()
                target_distribution = random.multinomial(cluster_size, transition_probabilities, size=1)[0]










        # pathways = []
        # for each in range(1):  # TODO: There should be while loop. To execute while last item of pathway does not equal 'Y'".
        #     pathway = ["X"]
        #     key = pathway[-1]
        #     transition_probabilities = transition_probabilities_by_sources[key]
        #     random = RandomState()
        #     next_location_sizes = random.multinomial(cluster_size, transition_probabilities, size=1)[0]
        #     for source_index, next_location_size in enumerate(next_location_sizes):
        #         for _ in range(next_location_size):
        #             new_pathway = pathway[:]
        #             new_pathway.append(sources[source_index][0])
        #             pathways.append(new_pathway)
        #     print(pathways)
        #     pass  # TODO: Implement a pathway generation.


if __name__ == '__main__':
    main()
