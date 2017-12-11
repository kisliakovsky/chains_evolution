from typing import List, Tuple, Union, Set, Iterable

from numpy.random import RandomState

from src import strings, maths

Letter = str
START_GENE = "X"
FINISH_GENE = "Y"


def obtain_evolution_subsequences(sequence: str):
    subsequences = strings.obtain_forward_substrings(sequence)
    return subsequences[2:-1]


class ChildGenerator(object):

    def __init__(self, parents: Iterable[str]):
        self.__genome_cores = [parent[1:-1] for parent in parents]
        self.__genome_lengths = self.__get_genome_lengths()
        self.__unique_lengths, self.__length_repetitions = self.__get_length_repetitions()
        self.__random = RandomState()
        self.__length_probabilities = self.__determine_length_probabilities()
        self.__gene_probabilities_by_position = self.__determine_genes_probabilities_by_position()
        self.__forbidden_lengths = set()

    def generate(self) -> Union[str, None]:
        length = self.__determine_length()
        while length in self.__forbidden_lengths:
            length = self.__determine_length()
        child = ""
        previous_letter = ""
        for i in range(length):
            curr_letter, next_letter = self.__produce_gene(i, i == (length - 1))
            while curr_letter == previous_letter:
                curr_letter, next_letter = self.__produce_gene(i, i == (length - 1))
                curr_codes, curr_probabilities, curr_random = self.__gene_probabilities_by_position[i]
                if len(curr_codes) == 2 and previous_letter in curr_codes and next_letter in curr_codes:
                    self.__forbidden_lengths.add(length)
                    return None
            child += curr_letter
            previous_letter = curr_letter
        return START_GENE + child + FINISH_GENE

    def __produce_gene(self, position: int, is_last: bool) -> Tuple[Letter, Letter]:
        curr_genes, curr_probabilities, curr_random = self.__gene_probabilities_by_position[position]
        index = list(curr_random.multinomial(1, curr_probabilities, size=1)[0]).index(1)
        if not is_last:
            next_genes, next_probabilities, next_random = self.__gene_probabilities_by_position[position + 1]
            if len(next_probabilities) == 1:
                next_gene = next_genes[0]
                i = curr_genes.index(next_gene) if next_gene in curr_genes else None
                if i is not None:
                    p = curr_probabilities[i] / (len(curr_probabilities) - 1)
                    new_curr_codes = curr_genes[:]
                    new_curr_probabilities = [curr_probability + p for curr_probability in curr_probabilities]
                    del new_curr_probabilities[i]
                    del new_curr_codes[i]
                    index = list(curr_random.multinomial(1, new_curr_probabilities, size=1)[0]).index(1)
                    return new_curr_codes[index], next_gene
        return curr_genes[index], ""

    def __get_genome_lengths(self):
        return [len(gene) for gene in self.__genome_cores]

    def __get_length_repetitions(self):
        return maths.count_repetitions(sorted(self.__genome_lengths))

    def __determine_length_probabilities(self):
        return [repetition / len(self.__genome_lengths) for repetition in self.__length_repetitions]

    def __determine_length(self):
        index = list(self.__random.multinomial(1, self.__length_probabilities, size=1)[0]).index(1)
        return self.__unique_lengths[index]

    def __determine_genes_probabilities_by_position(self) -> List[Tuple[List[Letter], List[float], RandomState]]:
        max_length = max(self.__unique_lengths)
        all_genes_probabilities = []
        for position in range(max_length):
            genes = []
            for genome_core in self.__genome_cores:
                if len(genome_core) - 1 < position:
                    continue
                gene = genome_core[position]
                genes.append(gene)
            unique_genes, genes_repetitions = maths.count_repetitions(sorted(genes))
            genes_probabilities = [repetition / len(genes) for repetition in genes_repetitions]
            all_genes_probabilities.append(tuple((unique_genes, genes_probabilities, RandomState())))
        return all_genes_probabilities
