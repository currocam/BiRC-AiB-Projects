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
if n < 3:
    raise ValueError("n should be equal or greater than 3")
S = list(range(n))
N = D.copy()
for i, j in np.ndindex(D.shape):
    ri = sum
    N[i, j] += (sum(D[:, i]) + sum(D[:, j]) )/(len(S)-2)
np.fill_diagonal(N, np.inf)
i, j = np.unravel_index(np.argmin(N), N.shape)

node_k = Clade(
    clades = [tree.clade.clades.pop(max(i, j)),tree.clade.clades.pop(min(i, j))], 
    )

gamma = (D[i, j] + sum(D[:, i]) - sum(D[:, j]))/2
node_k.clades[0].branch_length = gamma
node_k.clades[1].branch_length = D[i, j] - gamma
tree.clade.clades.append(node_k)
Phylo.draw_ascii(tree)
