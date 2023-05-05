import random
from hpview import HPFold, make_absfold


def path_to_grid(path: str) -> list[tuple[int, int]]:
    grid = [(0, 0)]
    for x in path:
        previous = grid[-1]
        match x:
            case "S":
                grid.append((previous[0], previous[1] - 1))
            case "N":
                grid.append((previous[0], previous[1] + 1))
            case "E":
                grid.append((previous[0] + 1, previous[1]))
            case "W":
                grid.append((previous[0] - 1, previous[1]))
    return grid


def grid_to_path(grid: list[tuple[int, int]]) -> str:
    grid = list(reversed(grid))
    previous_x, previous_y = grid.pop()
    path = list()
    while grid:
        val = grid.pop()
        if val == (previous_x, previous_y + 1):
            path.append("N")
        elif val == (previous_x, previous_y - 1):
            path.append("S")
        elif val == (previous_x + 1, previous_y):
            path.append("E")
        elif val == (previous_x - 1, previous_y):
            path.append("W")
        previous_x, previous_y = val
    return "".join(path)


def is_valid_path(path: str) -> bool:
    grid = path_to_grid(path)
    return len(grid) == len(set(grid))


def random_walk(grid: list[tuple[int, int]], steps: int) -> list[tuple[int, int]]:
    checks = set(grid)
    possibilities = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    size_undo = 1
    while steps > 0:
        random.shuffle(possibilities)
        is_invalid = True
        for move in possibilities:
            next_step = (grid[-1][0] + move[0], grid[-1][1] + move[1])
            if next_step not in checks:
                checks.add(next_step)
                grid.append(next_step)
                steps -= 1
                is_invalid = False
                break
        if is_invalid:
            steps += size_undo
            checks.difference_update(grid[len(grid) - size_undo : len(grid)])
            checks = set(grid)
            grid = grid[0 : len(grid) - size_undo]
            size_undo += 1
    return grid


def generate_random_path(n: int) -> str:
    grid = random_walk([(0, 0)], n - 1)
    return grid_to_path(list(grid))


def mutate_end_region(path: str, n: int) -> str:
    grid = path_to_grid(path)
    grid = random_walk(grid[0:n], n)
    return grid_to_path(grid)


def mutate_start_region(path: str, n: int) -> str:
    return mutate_end_region(path[::-1], n)[::-1]


hp = "pphhhphhhhhhhhppphhhhhhhhhhphppphhhhhhhhhhhhpppphhhhhhphhphp"
seq = HPFold(hp)

best_score = 0
best_path = "".join((len(hp) - 1) * ["S"])

for _ in range(50000):
    try:
        path = generate_random_path(len(hp))
        seq.SetAbsFold(make_absfold(path))
        score = seq.GetScore()
        if score > best_score:
            best_score, best_path = score, path
            print(score)
            for i in range(len(hp) // 5):
                for _ in range(i * 3):
                    path2 = mutate_end_region(path, i)
                    seq.SetAbsFold(make_absfold(path2))
                    score = seq.GetScore()
                    if score > best_score:
                        best_score, best_path = score, path2
                    path2 = mutate_start_region(path, i)
                    seq.SetAbsFold(make_absfold(path2))
                    score = seq.GetScore()
                    if score > best_score:
                        best_score, best_path = score, path2
    except:
        pass
    # print(f"Optimal value: {best_score}", end="\r")

seq = HPFold(hp)
seq.SetAbsFold(make_absfold(best_path))
seq.PrintFold()
