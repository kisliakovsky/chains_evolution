import jellyfish
from scipy.spatial import distance
import numpy


def calculate_nastya_distances(vectors):
    vectors = calculate_levenshtein_distances(vectors)
    return calculate_euclid_distances(vectors)


def calculate_euclid_distances(vectors):
    return _calculate_distances(vectors, distance.euclidean)


def calculate_levenshtein_distances(vectors):
    return _calculate_distances(vectors, jellyfish.levenshtein_distance)


def _calculate_distances(vectors, dist_method):
    dim = len(vectors)
    distances = numpy.zeros((dim, dim))
    for i in range(dim):
        distances[i][i] = 0
        for j in range(i + 1, dim):
            distances[i][j] = dist_method(vectors[i], vectors[j])
            distances[j][i] = distances[i][j]
    return distances


def calculate_distance(vector1: str, vector2: str) -> float:
    return jellyfish.damerau_levenshtein_distance(vector1, vector2)
