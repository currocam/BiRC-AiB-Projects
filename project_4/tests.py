from rfdist import *
from Bio import Phylo
from copy import deepcopy
import random

Tree = Phylo.Newick.Tree
def random_tree_generator(n: int)-> Tree:
    return Phylo.BaseTree.Tree.randomized(n)

def test_rfdist():
    for _ in range(100):
        n = random.randint(2, 30)
        tree1 = random_tree_generator(n)
        tree2 = random_tree_generator(n)
        assert rfdist(deepcopy(tree1), deepcopy(tree1)) == 0
        assert rfdist(deepcopy(tree2), deepcopy(tree2)) == 0
        assert rfdist(deepcopy(tree1), deepcopy(tree2)) == rfdist(deepcopy(tree2), deepcopy(tree1))
