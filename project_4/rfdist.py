import sys
from Bio import Phylo


def rfdist(T1, T2):
    # Step1: Root the two input trees at the same leaf

    # Find the node where to root the tree
    root1 = T1.common_ancestor({"name": "seq1"})
    root2 = T2.common_ancestor({"name": "seq1"})

    # Set the root of the trees
    T1.root_with_outgroup(root1)
    T2.root_with_outgroup(root2)

    # Step 2: Make a Depth-First numbering of the leaves in T1

    # Make a depth-first numbering of the leaves
    num = 1
    for leaf in T1.get_terminals():
        leaf.depthnum = num
        num += 1

    # Print the leaf nodes in depth-first order
    for leaf in sorted(T1.get_terminals(), key=lambda x: x.depthnum):
        print(leaf.name, leaf.depthnum)

    # Step 3: Rename the leaves in T2 with the DF-numbering of leaves in T1
    for node in T2.get_terminals():
        node_depthnum = None
        for leaf in T1.get_terminals():
            if leaf.name == node.name:
                node_depthnum = leaf.depthnum
                break
        if node_depthnum is not None:
            node.depthnum = node_depthnum
        else:
            raise ValueError(f"Leaf '{node.name}' not found in Tree1")

    # Step 4:
    # Annotate internal nodes in T1 with DF-intervals
    for clade in T1.find_clades():
        if not clade.is_terminal():
            leaves = [leaf.depthnum for leaf in clade.get_terminals()]
            clade.df_interval = (min(leaves), max(leaves))

    for clade in T1.find_clades():
        if not clade.is_terminal():
            print(clade.df_interval)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage: python rfdist.py tree1.new tree2.new")
    tree1 = Phylo.read(sys.argv[1], 'newick')
    tree2 = Phylo.read(sys.argv[2], 'newick')
    rfdist(tree1, tree2)