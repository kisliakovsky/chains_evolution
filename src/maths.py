from typing import List, Any, TypeVar, Tuple

import itertools

T = TypeVar('T')


def count_repetitions(sorted_items: List[T]) -> Tuple[List[int], List[int]]:
    keys = []
    counts = []
    for key, group in itertools.groupby(sorted_items):
        keys.append(key)
        counts.append(len(list(group)))
    return keys, counts
