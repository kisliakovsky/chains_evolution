from typing import List

from src.clusters_info import calc_cluster_distribution
from src.pathways import collect_pathways

NUMBER_OF_CLUSTERS = 10
POPULATION_SIZE = 100

CACHE = False
CACHED = {
    "distribution": [1, 34, 14, 4, 19, 8, 2, 6, 6, 6],
    "pathways": ['XAFIFEDY', 'XANFEY', 'XANFEY', 'XANFEY', 'XAFNIFEY', 'XAFNFEY', 'XAFNFEY', 'XAFNFEY', 'XAFNFEY',
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
    "favorite_pathway": 'XAFNIFEIFEY'
}


def main():
    if CACHE:
        pathways = CACHED["pathways"]
        favorite_pathway = CACHED["favorite_pathway"]
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
