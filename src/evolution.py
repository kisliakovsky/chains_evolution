from typing import List

from numpy.random import RandomState

from src import strings, maths

Letter = str


def obtain_evolution_subsequences(sequence: str):
    subsequences = strings.obtain_forward_substrings(sequence)
    return subsequences[2:]


class ChildGenerator(object):

    def __init__(self, parents: List[str]):
        self.__unique_genes = [parent[1:-1] for parent in parents]
        self.__gene_lengths = self.__get_gene_lengths()
        self.__unique_lengths, self.__length_repetitions = self.__get_length_repetitions()
        self.__random = RandomState()
        self.__length_probabilities = self.__determine_length_probabilities()
        self.__code_probabilities_by_position = self.__determine_code_probabilities_by_position()

    def generate(self) -> str:
        length = self.__determine_length()
        child = ""
        for i in range(length):
            child += self.__produce_gene(i)
        return "X" + child + "Y"

    def __produce_gene(self, position: int) -> Letter:
        codes, probabilities, random = self.__code_probabilities_by_position[position]
        index = list(random.multinomial(1, probabilities, size=1)[0]).index(1)
        return codes[index]

    def __get_gene_lengths(self):
        return [len(gene) for gene in self.__unique_genes]

    def __get_length_repetitions(self):
        return maths.count_repetitions(sorted(self.__gene_lengths))

    def __determine_length_probabilities(self):
        return [repetition / len(self.__gene_lengths) for repetition in self.__length_repetitions]

    def __determine_length(self):
        index = list(self.__random.multinomial(1, self.__length_probabilities, size=1)[0]).index(1)
        return self.__unique_lengths[index]

    def __determine_code_probabilities_by_position(self):
        max_length = max(self.__unique_lengths)
        all_code_probabilities = []
        for position in range(max_length):
            codes = []
            for gene in self.__unique_genes:
                if len(gene) - 1 < position:
                    continue
                code = gene[position]
                codes.append(code)
            unique_codes, code_repetitions = maths.count_repetitions(sorted(codes))
            code_probabilities = [repetition / len(codes) for repetition in code_repetitions]
            all_code_probabilities.append(tuple((unique_codes, code_probabilities, RandomState())))
        return all_code_probabilities
