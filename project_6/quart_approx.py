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
        if a > b:
            break
        matchs[a] = b
    return matchs


def get_match_even(evens: list[int], odds: list[int]) -> dict[int, int]:
    """
    >>> get_match_even([0, 2], [1, 3])
    {0: 3}
    >>> get_match_even([0, 4, 6], [1, 3, 5, 7])
    {0: 7, 4: 5}
    """
    return match_pairs(evens, odds)


def get_match_odds(evens: list[int], odds: list[int]) -> dict[int, int]:
    """
    >>> get_match_odds([0, 2], [1, 3])
    {1: 2}
    >>> get_match_odds([0, 4, 6], [1, 3, 5, 7])
    {1: 6, 3: 4}
    """
    return match_pairs(odds, evens)


evens, odds = find_even_odd("HHPHHHHH")
match_evens, match_odds = get_match_even(evens, odds), get_match_odds(evens, odds)
