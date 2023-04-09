from rfdist import *
from Bio import Phylo
from copy import deepcopy
import random

Tree = Phylo.Newick.Tree
def random_tree_generator(n: int)-> Tree:
    return Phylo.BaseTree.Tree.randomized(n)

def rfdist_with_copy(T1: Tree, T2: Tree)-> int:
    return rfdist(deepcopy(T1), deepcopy(T2))

def test_identity():
    # The distance of a tree with itself should be always zero¨
    for _ in range(100):
        n = random.randint(2, 30)
        tree1 = random_tree_generator(n)
        assert rfdist_with_copy(tree1, tree1) == 0

def test_symmetry():
    # The distance of a tree 1 and tree 2 should be always equal to the distance of tree 2 and tree 1. 
    for _ in range(100):
        n = random.randint(2, 30)
        tree1 = random_tree_generator(n)
        tree2 = random_tree_generator(n)
        assert rfdist_with_copy(tree1, tree2) == rfdist_with_copy(tree2, tree1)

def test_triangle_inequality():
    # The distance D(A, B) <= D(A, C) + D(C, B)
    for _ in range(100):
        n = random.randint(2, 30)
        treeA = random_tree_generator(n)
        treeB = random_tree_generator(n)
        treeC = random_tree_generator(n)
        assert rfdist_with_copy(treeA, treeB) <= rfdist_with_copy(treeA, treeC) + rfdist_with_copy(treeC, treeB)
