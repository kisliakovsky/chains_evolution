from src.clusters_info import calc_cluster_distribution
from src.pathways import collect_pathways

NUMBER_OF_CLUSTERS = 10
POPULATION_SIZE = 100

CACHE = True
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
                 'XAFNIFEDEY', 'XAFNIFEDEY', 'XAFNFEY']
}


def main():
    if CACHE:
        pathways = CACHED["pathways"]
    else:
        cluster_distribution = calc_cluster_distribution(POPULATION_SIZE, random_seed=47)
        pathways = collect_pathways(cluster_distribution)
    print(pathways)


if __name__ == '__main__':
    main()
