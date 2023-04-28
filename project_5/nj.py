import sys
import pandas as pd
import numpy as np
from Bio import Phylo
from Bio.Phylo.BaseTree import Clade

Tree = Phylo.Newick.Tree
Clade = Phylo.Newick.Clade


def read_phylip_file(file: str) -> tuple[np.ndarray, list[str]]:
    df = pd.read_csv(file, delimiter=" ", skiprows=[0], header=None)
    cols = df.pop(0)
    df.index = df.columns = cols
    return df.to_numpy(), cols.to_list()


def create_start_tree(leafs: list[str]):
    tree = Phylo.BaseTree.Tree(rooted=False)
    for leaf in leafs:
        tree.clade.clades.append(Phylo.BaseTree.Clade(name=leaf))
    return tree


def find_neighbours(D: np.ndarray) -> tuple[int, int]:
    val = np.inf
    sum_rows = [sum(D[:, i]) for i in range(D.shape[0])]
    sum_cols = [sum(D[:, j]) for j in range(D.shape[0])]
    for i, j in np.ndindex(D.shape):
        if i == j:
            continue
        N_ij = D[i, j] + (sum_rows[i] + sum_cols[j]) / (len(D) - 2)
        if val > N_ij:
            i_min, j_min = i, j
            val = N_ij
    return i_min, j_min


def join_neighbours(D: np.ndarray, clades: list[Clade], i: int, j: int):
    node = Clade(
        clades=[clades.pop(max(i, j)), clades.pop(min(i, j))],
    )
    gamma = (D[i, j] + sum(D[:, i]) - sum(D[:, j])) / 2
    node.clades[0].branch_length = gamma
    node.clades[1].branch_length = D[i, j] - gamma
    return node


def update_dissimilarity_matrix(D: np.ndarray, i: int, j: int):
    d_ij = D[i, j]
    row_i = D[i,]
    col_j = D[:, j]

    rows = [row for row in range(D.shape[0]) if row not in [i, j]]
    rows.append(i)
    cols = [col for col in range(D.shape[1]) if col not in [i, j]]
    cols.append(i)

    D = D[rows][:, cols]

    k = -1
    for m in range(len(D) - 1):
        D[k, m] = D[m, k] = 0.5 * (row_i[m] + col_j[m] - d_ij)
    return D


def terminate_nj(D: np.ndarray, clades: list[Clade]):
    i, j, m = 0, 1, 2

    node = Clade(
        clades=[
            clades.pop(m),
            clades.pop(j),
            clades.pop(i),
        ]
    )

    node.clades[i].branch_length = 0.5 * (D[i, j] + D[i, m] - D[j, m])
    node.clades[j].branch_length = 0.5 * (D[i, j] + D[j, m] - D[i, m])
    node.clades[m].branch_length = 0.5 * (D[i, m] + D[j, m] - D[i, j])
    return node


if __name__ == "__main__":
    D, leafs = read_phylip_file(sys.argv[1])
    tree = create_start_tree(leafs)
    clades = tree.clade.clades
    while len(D) > 3:
        if len(D) % 10 == 0:
            print(f"Iteration {len(D)}", file=sys.stderr)
        i, j = find_neighbours(D)
        knode = join_neighbours(D, clades, i, j)
        clades.append(knode)
        D = update_dissimilarity_matrix(D, i, j)
    final_node = terminate_nj(D, clades)
    clades.append(final_node)
    #
    tree = tree.common_ancestor(*tree.get_terminals())
    # Phylo.draw_ascii(tree)
    Phylo.write(tree, format="newick", file=sys.stdout)
