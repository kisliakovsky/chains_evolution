from src.clusters_info import calc_cluster_distribution
from src.pathways import collect_pathways

NUMBER_OF_CLUSTERS = 10
POPULATION_SIZE = 100

CACHE = True
CACHED_CLUSTER_DISTRIBUTION = [1, 34, 14, 4, 19, 8, 2, 6, 6, 6]


def main():
    if CACHE:
        cluster_distribution = CACHED_CLUSTER_DISTRIBUTION
    else:
        cluster_distribution = calc_cluster_distribution(POPULATION_SIZE, random_seed=47)
    pathways = collect_pathways(cluster_distribution)
    print(pathways)


if __name__ == '__main__':
    main()
