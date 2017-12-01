from src import strings


def obtain_evolution_subsequences(sequence: str):
    subsequences = strings.obtain_forward_substrings(sequence)
    return subsequences[2:]
