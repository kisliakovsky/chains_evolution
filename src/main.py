from src.dist_among_clusters import calc_cluster_distribution

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
        for each in range(cluster_size):
            pass  # TODO: Implement a pathway generation.


if __name__ == '__main__':
    pass
