import jellyfish
from scipy.spatial import distance
import numpy


def calculate_nastya_distances(vectors):
    vectors = calculate_levenshtein_distances(vectors)
    vectors = calculate_default_distances(vectors)
    return vectors


def calculate_euclid_distances(vectors):
    return _calculate_distances(vectors, distance.euclidean)


def calculate_squared_euclid_distances(vectors):
    return _calculate_distances(vectors, calculate_squared_euclid_distance)


def calculate_levenshtein_distances(vectors):
    return _calculate_distances(vectors, jellyfish.levenshtein_distance)


def calculate_default_distances(vectors):
    return _calculate_distances(vectors, calculate_default_distance)


def calculate_euclid_distance(x, y):
    return distance.euclidean(x, y)


def calculate_squared_euclid_distance(x, y):
    return distance.euclidean(x, y) ** 2


def calculate_levenshtein_distance(x, y):
    return jellyfish.levenshtein_distance(x, y)


def calculate_default_distance(x, y):
    return calculate_squared_euclid_distance(x, y)


def _calculate_distances(vectors, dist_method):
    dim = len(vectors)
    distances = numpy.zeros((dim, dim))
    for i in range(dim):
        distances[i][i] = 0
        for j in range(i + 1, dim):
            distances[i][j] = dist_method(vectors[i], vectors[j])
            distances[j][i] = distances[i][j]
    return distances
