from typing import List

from src.clusters_info import calc_cluster_distribution
from src.pathways import collect_pathways, collect_unique_pathways, select_favorite_pathway, filter_pathways
from src import graph_building, graph_exporting, evolution
from src import strings

POPULATION_SIZE = 100

POPULATION_SIZE_KEY = "population_size"
DISTRIBUTION_KEY = "distribution"
PATHWAYS_KEY = "pathways"
UNIQUE_PATHWAYS_KEY = "unique_pathways"
FAVORITE_PATHWAY_KEY = "favorite_pathway"
FAVORITE_SUBPATHWAYS_KEY = "favorite_subpathways"

CACHE = True
CACHED = {
    POPULATION_SIZE_KEY: 100,
    DISTRIBUTION_KEY: [1, 34, 14, 4, 19, 8, 2, 6, 6, 6],
    PATHWAYS_KEY: ['XAEFEDY', 'XANFEDEY', 'XAFNIFEY', 'XAFNFEDY', 'XAFNFEDY', 'XAFNFEDY', 'XAFNFEY', 'XAFNFEY',
                   'XAFNFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY',
                   'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY',
                   'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY', 'XAFIFEY',
                   'XANFIDY', 'XAIY', 'XAFEDY', 'XAFEY', 'XAFEY', 'XAFEY', 'XAFEY', 'XAFDY', 'XAFDY', 'XAFY', 'XAFY',
                   'XAFY', 'XAFY', 'XAFY', 'XAFNIFEDY', 'XAFNIFEDY', 'XAFNIFEDY', 'XAFNFNIFEIFEY', 'XAFNIFEDY',
                   'XAFNIFEDY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY',
                   'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY', 'XAFNIFEY',
                   'XAFNIFEY', 'XAFNFIFEY', 'XANIFEFDY', 'XAIEDY', 'XAFIFIFY', 'XAFIFEIFEDY', 'XAFIFEDY', 'XAFIFEDY',
                   'XAFIFEDY', 'XAFEDY', 'XAFNFEFIFEY', 'XAEDY', 'XAIFEY', 'XAIFEY', 'XAIEY', 'XAFIFEY', 'XAFIEY',
                   'XAFIDY', 'XANFDY', 'XAFNIFY', 'XAFNIFY', 'XAFNIFY', 'XAFNIEY', 'XAFEIEY', 'XAFNIFEDEY',
                   'XAFNIFEDEY', 'XAFNIFEDEY', 'XAFNIFEDEY', 'XAFNIFEDEY', 'XAFNFEDEY'],
    UNIQUE_PATHWAYS_KEY: ['XANFIDY', 'XAFNIFY', 'XAFNIFEDEY', 'XANFDY', 'XAFEDY', 'XAFNIFEDY', 'XAFNFEDY', 'XAIEDY',
                          'XAIEY', 'XAEDY', 'XAFEY', 'XANFEDEY', 'XAIFEY', 'XAFY', 'XAFIFEIFEDY', 'XAFNFNIFEIFEY',
                          'XAEFEDY', 'XANIFEFDY', 'XAIY', 'XAFNFEFIFEY', 'XAFNFEDEY', 'XAFIFEDY', 'XAFDY', 'XAFIDY',
                          'XAFIFIFY', 'XAFNIEY', 'XAFIEY', 'XAFNFEY', 'XAFNFIFEY', 'XAFEIEY', 'XAFNIFEY', 'XAFIFEY'],
    FAVORITE_PATHWAY_KEY: 'XAEFEDY',
    FAVORITE_SUBPATHWAYS_KEY: ['XAE', 'XAEF', 'XAEFE', 'XAEFED', 'XAEFEDY']
}


def main():
    if CACHE:
        cluster_distribution = CACHED[DISTRIBUTION_KEY]
        pathways = CACHED[UNIQUE_PATHWAYS_KEY]
        favorite_subpathways = CACHED[FAVORITE_SUBPATHWAYS_KEY]
    else:
        cluster_distribution = calc_cluster_distribution(POPULATION_SIZE, random_seed=47)
        pathways = collect_unique_pathways(cluster_distribution)
        favorite_pathway = select_favorite_pathway(pathways)
        favorite_subpathways = evolution.obtain_evolution_subsequences(favorite_pathway)
    # first_subpathway = favorite_subpathways[0]
    # filtered_pathways = filter_pathways(pathways, first_subpathway)
    # print(filtered_pathways)
    graph_exporting.save_for_cytoscape(pathways, "main")
    graph_exporting.save_for_gephi(pathways, "main")


if __name__ == '__main__':
    main()
