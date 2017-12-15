from typing import TypeVar, List, Tuple, Dict

import jellyfish

T = TypeVar('T')
TList = List[T]
IDX_KEY = 'idx'
NEW_IDX_KEY = 'new_idx'
COUNT_KEY = 'count'


def remove_item_from_list(item_to_remove: T, items: TList) -> Tuple[int, TList]:
    new_items = []
    removed_items_count = 0
    for item in items:
        if item_to_remove == item:
            removed_items_count += 1
        else:
            new_items.append(item)
    return removed_items_count, new_items


def remove_item_from_matrix(item_to_remove: T, matrix: List[List[T]]) -> Tuple[int, List[List[T]]]:
    new_matrix = []
    matrix_removed_count = 0
    for items in matrix:
        removed_items_count, new_items = remove_item_from_list(item_to_remove, items)
        new_matrix.append(new_items)
        matrix_removed_count += removed_items_count
    return matrix_removed_count, new_matrix


def transform_matrix_to_dict(matrix: List[List[T]]) -> Dict[T, Dict[str, int]]:
    items_dict = {}
    for i, items in enumerate(matrix):
        for item in items:
            item_obj = items_dict.get(item, None)
            if item_obj is not None:
                item_obj[COUNT_KEY] += 1
            else:
                items_dict[item] = {
                    IDX_KEY: i,
                    COUNT_KEY: 1
                }
    return items_dict


def merge_matrix_dicts(dict1: Dict[T, Dict[str, int]], dict2: Dict[T, Dict[str, int]]):
    for k, v in dict1.items():
        item_obj = dict2.get(k, None)
        if item_obj is not None:
            v[COUNT_KEY] += item_obj[COUNT_KEY]
            del dict2[k]
    return dict1, dict2
