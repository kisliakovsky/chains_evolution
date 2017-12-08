from typing import List, Tuple, Union, Set, Iterable

from numpy.random import RandomState

from src import strings, maths

Letter = str


def obtain_evolution_subsequences(sequence: str):
    subsequences = strings.obtain_forward_substrings(sequence)
    return subsequences[2:-1]


class ChildGenerator(object):

    def __init__(self, parents: Iterable[str]):
        self.__unique_genes = [parent[1:-1] for parent in parents]
        self.__gene_lengths = self.__get_gene_lengths()
        self.__unique_lengths, self.__length_repetitions = self.__get_length_repetitions()
        self.__random = RandomState()
        self.__length_probabilities = self.__determine_length_probabilities()
        self.__code_probabilities_by_position = self.__determine_code_probabilities_by_position()
        self.__forbidden_lengths = set()

    def generate(self) -> Union[str, None]:
        length = self.__determine_length()
        while length in self.__forbidden_lengths:
            length = self.__determine_length()
        child = ""
        previous_letter = ""
        for i in range(length):
            curr_letter, next_letter = self.__produce_letter(i, i == (length - 1))
            while curr_letter == previous_letter:
                curr_letter, next_letter = self.__produce_letter(i, i == (length - 1))
                curr_codes, curr_probabilities, curr_random = self.__code_probabilities_by_position[i]
                if len(curr_codes) == 2 and previous_letter in curr_codes and next_letter in curr_codes:
                    self.__forbidden_lengths.add(length)
                    return None
            child += curr_letter
            previous_letter = curr_letter
        return "X" + child + "Y"

    def __produce_letter(self, position: int, is_last: bool) -> Tuple[Letter, Letter]:
        curr_codes, curr_probabilities, curr_random = self.__code_probabilities_by_position[position]
        index = list(curr_random.multinomial(1, curr_probabilities, size=1)[0]).index(1)
        if not is_last:
            next_codes, next_probabilities, next_random = self.__code_probabilities_by_position[position + 1]
            if len(next_probabilities) == 1:
                next_code = next_codes[0]
                i = curr_codes.index(next_code) if next_code in curr_codes else None
                if i is not None:
                    p = curr_probabilities[i] / (len(curr_probabilities) - 1)
                    new_curr_codes = curr_codes[:]
                    new_curr_probabilities = [curr_probability + p for curr_probability in curr_probabilities]
                    del new_curr_probabilities[i]
                    del new_curr_codes[i]
                    index = list(curr_random.multinomial(1, new_curr_probabilities, size=1)[0]).index(1)
                    return new_curr_codes[index], next_code
        return curr_codes[index], ""

    def __get_gene_lengths(self):
        return [len(gene) for gene in self.__unique_genes]

    def __get_length_repetitions(self):
        return maths.count_repetitions(sorted(self.__gene_lengths))

    def __determine_length_probabilities(self):
        return [repetition / len(self.__gene_lengths) for repetition in self.__length_repetitions]

    def __determine_length(self):
        index = list(self.__random.multinomial(1, self.__length_probabilities, size=1)[0]).index(1)
        return self.__unique_lengths[index]

    def __determine_code_probabilities_by_position(self) -> List[Tuple[List[Letter], List[float], RandomState]]:
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
