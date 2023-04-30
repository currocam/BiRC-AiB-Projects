import sys
from Bio import Phylo
from typing import List, Tuple

# Define helper types
Tree = Phylo.Newick.Tree
Clade = Phylo.Newick.Clade

def root_at_same_leaf(T1: Tree, T2: Tree)-> Tuple[Tree, Tree]:
    # Find the node where to root the tree
    root1 = T1.get_terminals()[0] # Arbitrarily first leaf
    root2 = next(T2.find_clades(root1.name))
    # Set the root of the trees
    T1.root_with_outgroup(root1)
    T2.root_with_outgroup(root2)
    # Remove outgroup
    T1.collapse(root1)
    T2.collapse(root2)
    return (
        T1.common_ancestor(x for x in T1.get_terminals()),
        T2.common_ancestor(x for x in T2.get_terminals())
    )

def is_potential_split(depths: List[int])-> bool:
    return max(depths) - min(depths) + 1 == len(depths)

def rfdist(T1: Tree, T2: Tree)-> int:
    size_T1, size_T2 = len(T1.get_terminals()), len(T1.get_terminals())
    if size_T1 != size_T2:
        raise ValueError('Tree 1 and Tree 2 have different length')
    if size_T1 < 3:
        return 0
    # Step1: Root the two input trees at the same leaf
    T1, T2 = root_at_same_leaf(T1, T2)
    # Step 2: Make a Depth-First numbering of the leaves in T1
    # No need to reannotate, we can just use a dictionary
    # and keep track of the names if we assume all headers are unique
    depth_dict = {leaf.name : num +1 for num, leaf in enumerate(T1.get_terminals()) if leaf.name}
    # Step 3:
    # Annotate internal nodes in T1 with DF-intervals
    intervals = set()
    for clade in T1.get_nonterminals():
        depths = [depth_dict[leaf.name] for leaf in clade.get_terminals() if leaf.name]
        intervals.add((min(depths), max(depths)))
    # Step 4
    # Count the number of shared splits'
    shared = 0
    for clade in T2.get_nonterminals():
        depths = [depth_dict[leaf.name] for leaf in clade.get_terminals() if leaf.name]
        if is_potential_split(depths) and (min(depths), max(depths)) in intervals:
            shared+=1
    #“number of splits in T1 and T2” - 2 * shared
    return len(intervals)*2 - 2*shared
    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage: python rfdist.py tree1.new tree2.new")
    tree1 = Phylo.read(sys.argv[1], 'newick')
    tree2 = Phylo.read(sys.argv[2], 'newick')
    print(rfdist(tree1, tree2))