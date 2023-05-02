from collections import OrderedDict

FORWARD, LEFT, RIGHT = "f", "l", "r"


def find_even_odd(hp: str) -> tuple[list[int], list[int]]:
    """
    >>> find_even_odd("HHH")
    ([0, 2], [1])
    >>> find_even_odd("HPH")
    ([0, 2], [])
    """
    evens, odds = list(), list()
    for i, x in enumerate(hp):
        if x == "H" and i % 2 == 0:
            evens.append(i)
        if x == "H" and i % 2 == 1:
            odds.append(i)
    return evens, odds


def match_pairs(x: list[int], y: list[int]) -> dict[int, int]:
    matchs = dict()
    for a, b in zip(x, reversed(y)):
        if a + 1 >= b:
            break
        matchs[a] = b
    return matchs


def get_match_even(evens: list[int], odds: list[int]) -> dict[int, int]:
    """
    >>> get_match_even([0, 2], [1, 3])
    {0: 3}
    >>> get_match_even([0, 4, 6], [1, 3, 5, 7])
    {0: 7}
    """
    return match_pairs(evens, odds)


def get_match_odds(evens: list[int], odds: list[int]) -> dict[int, int]:
    """
    >>> get_match_odds([0, 2], [1, 3])
    {1: 2}
    >>> get_match_odds([0, 4, 6], [1, 3, 5, 7])
    {1: 6}
    """
    return match_pairs(odds, evens)

    # Find P, at least half the odd-H’s are in one substring
    # on one side of p (the odd substring) and at least half the even-H’s are
    # on the other side of p (the even substring).


def split_binary_search(size, matchs):
    high, low = size, 0
    while True:
        split = (high - low) // 2
        at_least_half_odd = sum([x < split for x, _ in matchs]) / len(matchs) > 0.5
        at_least_half_even = sum([x > split for _, x in matchs]) / len(matchs) > 0.5
        if at_least_half_odd and at_least_half_even:
            return split
        if at_least_half_odd:
            low = split
        if at_least_half_even:
            high = split


if __name__ == "__main__":
    hp = "pphhhphhhhhhhhppphhhhhhhhhhphppphhhhhhhhhhhhpppphhhhhhphhphp".upper()
    evens, odds = find_even_odd(hp)
    match_evens, match_odds = get_match_even(evens, odds), get_match_odds(evens, odds)

    if len(match_evens) > len(match_odds):
        matchs = list(OrderedDict(sorted(match_evens.items())).items())
    else:
        matchs = list(OrderedDict(sorted(match_odds.items())).items())

    split = split_binary_search(len(hp), matchs)
    # Create straight line
    path = (len(hp) - 1) * [FORWARD]

    # Split into S1 and S2
    path[split : split + 2] = [RIGHT, RIGHT]

    evens = [e for e in evens if e < split]
    for index in range(len(evens) - 2 + 1):
        first, last = evens[index], evens[index + 1]
        size = last - first
        if size >= 4:
            path[first] = LEFT
            middle = first + size // 2
            path[middle - 1 : middle + 1] = [RIGHT, RIGHT]
            path[last - 1] = LEFT

    odds = [o for o in odds if o > split]
    for index in range(len(odds) - 2 + 1):
        first, last = odds[index], odds[index + 1]
        size = last - first
        if size >= 4:
            path[first] = LEFT
            middle = first + size // 2
            path[middle - 1 : middle + 1] = [RIGHT, RIGHT]
            path[last - 1] = LEFT

    print("".join(path))
