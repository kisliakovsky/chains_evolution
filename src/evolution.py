from typing import List

from src import strings


def obtain_evolution_subsequences(sequence: str):
    subsequences = strings.obtain_forward_substrings(sequence)
    return subsequences[2:]


class ChildGenerator(object):

    def __init__(self, parents: List[str]):
        self.__parents = parents

    def generate(self) -> str:
        pass
