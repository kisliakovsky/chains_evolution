import jellyfish
import numpy


def calculate_distances(vectors):
    dim = len(vectors)
    distances = numpy.zeros((dim, dim))
    for i in range(dim):
        for j in range(dim):
            distances[i][j] = jellyfish.damerau_levenshtein_distance(vectors[i], vectors[j])
    return distances
