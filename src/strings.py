def get_forward_substrings(string: str):
    substrings = []
    for i in range(len(string) - 1, 0, -1):
        substring = string[:-i]
        substrings.append(substring)
    substrings.append(string)
    return substrings
