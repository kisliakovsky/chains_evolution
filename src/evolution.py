from typing import List

from numpy.random import RandomState

from src import strings, maths


def obtain_evolution_subsequences(sequence: str):
    subsequences = strings.obtain_forward_substrings(sequence)
    return subsequences[2:]


class ChildGenerator(object):

    def __init__(self, parents: List[str]):
        parents = ["XABCY", "XDEFGY", "XHIJKLMY", "XHIFGY", "XABJKLMY"]
        self.__unique_genes = [parent[1:-1] for parent in parents]
        self.__random = RandomState()

    def generate(self) -> str:
        length = self.__determine_length()
        child = ""
        for i in range(length):
            child += "A"
        return "X" + child + "Y"

    def __determine_length(self):
        lengths = [len(gene) for gene in self.__unique_genes]
        unique_lengths, lengths_repetitions = maths.count_repetitions(sorted(lengths))
        lengths_probabilities = [repetition / len(lengths) for repetition in lengths_repetitions]
        length_index = list(self.__random.multinomial(1, lengths_probabilities, size=1)[0]).index(1)
        return unique_lengths[length_index]


print(ChildGenerator([]).generate())
