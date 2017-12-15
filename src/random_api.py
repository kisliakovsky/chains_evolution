from typing import Union, List

from numpy.random import RandomState
# noinspection PyPep8Naming
from numpy import ndarray as NDArray

ProbabilityList = Union[List[float], NDArray]
DistributionList = Union[List[int], NDArray]


def get_next_multinomial_dist_once(probs: ProbabilityList, size: int) -> DistributionList:
    return get_next_multinomial_dist(RandomState(), probs, size)


def get_next_multinomial_idx(rand: RandomState, probs: ProbabilityList) -> int:
    return list(get_next_multinomial_dist(rand, probs, 1)).index(1)


def get_next_multinomial_dist(rand: RandomState, probs: ProbabilityList, size: int) -> DistributionList:
    return rand.multinomial(size, probs, size=1)[0]
