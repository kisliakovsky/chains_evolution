import jellyfish
import numpy


def calculate_distances(vectors):
    dim = len(vectors)
    distances = numpy.zeros((dim, dim))
    for i in range(dim):
        distances[i][i] = 0
        for j in range(i + 1, dim):
            distances[i][j] = jellyfish.levenshtein_distance(vectors[i], vectors[j])
            distances[j][i] = distances[i][j]
    return distances
