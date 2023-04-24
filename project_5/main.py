import pandas as pd
import numpy as np
from Bio import Phylo
from Bio.Phylo.BaseTree import Clade
def read_phylip_file(file):
    df = pd.read_csv(file, delimiter=" ", skiprows = [0], header=None)
    cols = df.pop(0)
    df.index = df.columns = cols
    return df.to_numpy(), cols.to_list()

def create_start_tree(leafs):
    tree = Phylo.BaseTree.Tree(rooted = False)
    for leaf in leafs:
        tree.clade.clades.append(Phylo.BaseTree.Clade(name = leaf))
    return tree

D, leafs = read_phylip_file('project_5/tests/example_slide4.phy')
tree = create_start_tree(leafs)
Phylo.draw_ascii(tree)
n = len(D)

while len(D)> 3:
    N = D.copy()
    for i, j in np.ndindex(D.shape):
        ri = sum
        N[i, j] += (sum(D[:, i]) + sum(D[:, j]) )/(len(D)-2)
    np.fill_diagonal(N, np.inf)
    i, j = np.unravel_index(np.argmin(N), N.shape)

    node_k = Clade(
        clades = [tree.clade.clades.pop(max(i, j)),tree.clade.clades.pop(min(i, j))], 
        )

    gamma = (D[i, j] + sum(D[:, i]) - sum(D[:, j]))/2
    node_k.clades[0].branch_length = gamma
    node_k.clades[1].branch_length = D[i, j] - gamma
    tree.clade.clades.append(node_k)
    
    d_ij = D[i, j]
    row_i = np.delete(D[i,], (i, j))
    col_j = np.delete(D[:, j], (i, j))

    D = np.delete(D, (i, j), axis = 0)
    D = np.delete(D, (i, j), axis = 1)

    D = np.vstack((D, np.zeros(len(D))))
    D = np.hstack((D, np.zeros(len(D)).reshape(-1, 1)))

    k = -1
    for m in range(len(D)-1):
        D[k, m] = D[m, k] = 0.5*(row_i[m]+col_j[m]- d_ij)

i,j, m = 0, 1, 2

node_k = Clade(
        clades = [tree.clade.clades.pop(m),tree.clade.clades.pop(j),tree.clade.clades.pop(i),
    ])

node_k.clades[i].branch_length = 0.5*(D[i, j]+D[i, m]-D[j, m])
node_k.clades[j].branch_length = 0.5*(D[i, j]+D[j, m]-D[i, m])
node_k.clades[m].branch_length = 0.5*(D[i, m]+D[j, m]-D[i, j])
tree.clade.clades.append(node_k)
Phylo.draw_ascii(tree)
