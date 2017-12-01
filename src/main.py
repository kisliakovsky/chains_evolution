from typing import List

from src.clusters_info import calc_cluster_distribution
from src.pathways import collect_pathways

POPULATION_SIZE = 100

POPULATION_SIZE_KEY = "population_size"
DISTRIBUTION_KEY = "distribution"
PATHWAYS_KEY = "pathways"
FAVORITE_PATHWAY_KEY = "favorite_pathway"

CACHE = False
CACHED = {
    POPULATION_SIZE_KEY: 100,
    DISTRIBUTION_KEY: [1, 34, 14, 4, 19, 8, 2, 6, 6, 6],
    PATHWAYS_KEY: ['XAFIFEDY', 'XANFEY', 'XANFEY', 'XANFEY', 'XAFNIFEY', 'XAFNFEY', 'XAFNFEY', 'XAFNFEY', 'XAFNFEY',
                 'XAFNFEY', 'XAFNFEY', 'XAFNFEY', 'XAFNFEY', 'XAFNFEY', 'XAFINFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY',
                 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY',
                 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAIEY',
                 'XAIEY', 'XAFNY', 'XAFEY', 'XAFEY', 'XAFEY', 'XAFEY', 'XAFEY', 'XAFEY', 'XAFEY', 'XAFEY', 'XAFEY',
                 'XAFDY', 'XADFY', 'XAFNINIFEY', 'XAFNIFEIFEY', 'XAFNIFEIFY', 'XAFNIEIFY', 'XAFNIFEDY', 'XAFNIFEDY',
                 'XAFNIFEDY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY',
                 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY',
                 'XAFNIFEY', 'XANIFEDY', 'XAFIFEDY', 'XAFIFEDY', 'XAFIFEDY', 'XAFIFEDY', 'XAFIFDY', 'XADY', 'XADY',
                 'XAFNIFEDY', 'XAFNIFEDY', 'XAIFEY', 'XAIFEY', 'XAIFEY', 'XAIFY', 'XAIEY', 'XAFIEY', 'XAFNIFY',
                 'XAFNFDY', 'XAFNFDY', 'XAFEIEDY', 'XAFEFDY', 'XAFEDY', 'XAFNIFEDEY', 'XAFNIFEDEY', 'XAFNIFEDEY',
                 'XAFNIFEDEY', 'XAFNIFEDEY', 'XAFNFEY'],
    FAVORITE_PATHWAY_KEY: 'XAFNIFEIFEY'
}


def main():
    if CACHE:
        pathways = CACHED[PATHWAYS_KEY]
        favorite_pathway = CACHED[FAVORITE_PATHWAY_KEY]
    else:
        cluster_distribution = calc_cluster_distribution(POPULATION_SIZE, random_seed=47)
        pathways = collect_pathways(cluster_distribution)
        favorite_pathway = select_favorite_pathway(pathways)
    print(pathways)
    print(favorite_pathway)


def select_favorite_pathway(pathways: List[str]):
    index = len(pathways) // 2
    return pathways[index]


if __name__ == '__main__':
    main()
