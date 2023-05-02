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


def make_turn(path: list[int]) -> None:
    n = len(path)
    if n == 1:
        return path
    path[(n // 2) : (n // 2 + 2)] = [LEFT, LEFT]
    return path


def make_turn(path: list[int]) -> list[int]:
    n = len(path)
    if n == 1:
        return RIGHT
    path[(n // 2) : (n // 2 + 2)] = [RIGHT, RIGHT]
    return path


hp = "ppphhpphhhhpphhhphhphhphhhhpppppppphhhhhhpphhhhhhppppppppphphhphhhhhhhhhhhpphhhphhphpphphhhpppppphhh".upper()
evens, odds = find_even_odd(hp)
match_evens, match_odds = get_match_even(evens, odds), get_match_odds(evens, odds)

if len(match_evens) > len(match_odds):
    matchs = list(OrderedDict(sorted(match_evens.items())).items())
else:
    matchs = list(OrderedDict(sorted(match_odds.items())).items())

path = (len(hp) - 1) * [FORWARD]

k, v = matchs.pop()
path[k:v] = make_turn(path[k:v])
split = (v - k) // 2 + k
upper_count, lower_count = 0, 0
while matchs:
    k, v = matchs.pop()
    diff = (split - k - upper_count) - (v - split - 1 + lower_count)
    if diff < 0:
        lower_count -= diff
        path[v + diff - 2 : v + (diff + 2)] = [LEFT, RIGHT, RIGHT, LEFT]
    if diff > 0:
        upper_count += diff
        path[k + diff - 2 : k + diff + 2] = [LEFT, RIGHT, RIGHT, LEFT]


"".join(path)
