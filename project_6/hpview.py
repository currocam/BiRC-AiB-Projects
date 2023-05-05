#  hpview.py
#
#  Displays a 2D HP folding
#
#  Usage:
#
#  hpview.py <seq> <fold>
#
#  where <seq> is a string over the alphabet {h,p} and <fold> is a
#  folding of the string in either relative or absolute format.
#
#  A folding in relative format is a sequence over {f,l,r}, which
#  describes the fold as a sequence of steps (f)orward, (l)left, or
#  (r)ight.
#
#  A folding in absolute format is a sequence over {n,s,e,w}, which
#  describes the fold as a sequence of steps to the (n)orth, (s)outh,
#  (e)east, or (w)est.
#
#  History:
#
#  31-Oct-2007: Initial version.
#  30-Nov-2007: Hydrophobes at even positions are drawn as 'H' and
#  hydrophobes at odd positions are drawn as 'h'.
#  28-Oct-2008: Fixed counting of score.
#  05-Dec-2015: Small changes (print and has_key) to adapt to Python 3.
#
#  Christian Storm Pedersen <cstorm@birc.au.dk>.

import sys

#####################################################################
# Functions
#####################################################################


class HPFold:
    def __init__(self, s):
        legal = {"h": "h", "p": "p", "H": "h", "P": "p"}
        self.seq = []
        i = 1
        for c in s:
            if c in legal.keys():
                if legal[c] == "h" and i % 2 == 0:
                    self.seq.append("H")
                else:
                    self.seq.append(legal[c])
                i = i + 1

    def __len__(self):
        return len(self.seq)

    def SetRelFold(self, relfold):
        """
        Fold seq according to a description in relavtive format, i.e.
        a sequence of {f,l,r}'s which describe each step as (f)orward,
        (l)eft, or (r)ight.
        """
        turn = {"f": 0, "l": -1, "r": 1}
        direction = {0: "e", 1: "s", 2: "w", 3: "n"}
        absfold = []
        curr = 0
        for relstep in relfold:
            absstep = (curr + turn[relstep]) % 4
            absfold.append(direction[absstep])
            curr = absstep
        return self.SetAbsFold(absfold)

    def SetAbsFold(self, absfold):
        """
        Fold seq according to a description in absolute format, i.e.
        s sequence of {n,s,e,w}'s which describe each step as (n)orth,
        (s)outh, (e)ast, or (w)est.
        """
        self.legal_fold = (True, 0)
        self.grid = {}
        self.grid[0, 0] = [0]
        i = j = self.min_i = self.max_i = self.min_j = self.max_j = 0
        k = 1
        for step in absfold:
            if step == "n":
                i = i - 1
            elif step == "s":
                i = i + 1
            elif step == "e":
                j = j + 1
            elif step == "w":
                j = j - 1
            if (i, j) in self.grid.keys():
                self.legal_fold = (False, k)
                self.grid[i, j].append(k)
            else:
                self.grid[i, j] = [k]
            k = k + 1
            self.min_i = min(i, self.min_i)
            self.max_i = max(i, self.max_i)
            self.min_j = min(j, self.min_j)
            self.max_j = max(j, self.max_j)
        return self.legal_fold[0]

    def ContainNeighbors(self, l1, l2):
        """
        Returns true if there exists k1 in l1 and k2 in l2 such that
        abs(k1-k2) is 1, i.e. if the indices in l1 and l2 contain a
        pair of neighbors in seq.
        """
        res = False
        for k1 in l1:
            for k2 in l2:
                if abs(k1 - k2) == 1:
                    res = True
        return res

    def ContainHHs(self, l1, l2):
        """
        Returns true if there exists k1 in l1 and k2 in l2 where there
        is a 'h' at position k1 and k2 in seq, i.e. if the indices in
        l1 and l2 contain a pair which can make a h-h bond.
        """
        res = False
        for k1 in l1:
            for k2 in l2:
                if (self.seq[k1] == "h" or self.seq[k1] == "H") and (
                    self.seq[k2] == "h" or self.seq[k2] == "H"
                ):
                    res = True
        return res

    def GetScore(self):
        score = 0
        for i in range(self.min_i, self.max_i + 1):
            for j in range(self.min_j, self.max_j + 1):
                if (i, j) in self.grid.keys():
                    l1 = self.grid[i, j]
                    if (i, j + 1) in self.grid.keys():
                        l2 = self.grid[i, j + 1]
                        if self.ContainNeighbors(l1, l2):
                            pass  # print("-", end="")
                        elif self.ContainHHs(l1, l2):
                            # print("*", end="")
                            score = score + 1
                        else:
                            pass  # print(" ", end="")
                    else:
                        pass  # print(" ", end="")
                else:
                    pass  # print(".", end="")
                    pass  # print(" ", end="")
            # print()

            for j in range(self.min_j, self.max_j + 1):
                if (i, j) in self.grid.keys() and (i + 1, j) in self.grid.keys():
                    l1 = self.grid[i, j]
                    l2 = self.grid[i + 1, j]
                    if self.ContainNeighbors(l1, l2):
                        pass  # print("|", end="")
                    elif self.ContainHHs(l1, l2):
                        # print("*", end="")
                        score = score + 1
                    else:
                        pass  # print(" ", end="")
                else:
                    pass  # print(" ", end="")
                # print(" ", end="")
            # print()
        if self.legal_fold[0]:
            return score
        return -1

    def PrintFold(self):
        """
        Print fold and output its score
        """
        score = 0
        print()
        for i in range(self.min_i, self.max_i + 1):
            for j in range(self.min_j, self.max_j + 1):
                if (i, j) in self.grid.keys():
                    l1 = self.grid[i, j]
                    if len(l1) == 1:
                        print(self.seq[l1[0]], end="")
                    else:
                        print("X", end="")
                    if (i, j + 1) in self.grid.keys():
                        l2 = self.grid[i, j + 1]
                        if self.ContainNeighbors(l1, l2):
                            print("-", end="")
                        elif self.ContainHHs(l1, l2):
                            print("*", end="")
                            score = score + 1
                        else:
                            print(" ", end="")
                    else:
                        print(" ", end="")
                else:
                    print(".", end="")
                    print(" ", end="")
            print()

            for j in range(self.min_j, self.max_j + 1):
                if (i, j) in self.grid.keys() and (i + 1, j) in self.grid.keys():
                    l1 = self.grid[i, j]
                    l2 = self.grid[i + 1, j]
                    if self.ContainNeighbors(l1, l2):
                        print("|", end="")
                    elif self.ContainHHs(l1, l2):
                        print("*", end="")
                        score = score + 1
                    else:
                        print(" ", end="")
                else:
                    print(" ", end="")
                print(" ", end="")
            print()
        if self.legal_fold[0]:
            print("Score: %d" % (score))
        else:
            print("Illegal fold after %d steps" % (self.legal_fold[1]))


#####################################################################
# Functions
#####################################################################


def make_absfold(f):
    absfold = []
    for c in f.lower():
        if c == "n" or c == "s" or c == "e" or c == "w":
            absfold.append(c)
    return absfold


def make_relfold(f):
    relfold = []
    for c in f.lower():
        if c == "f" or c == "l" or c == "r":
            relfold.append(c)
    return relfold


def print_usage():
    print(
        """
Usage:

hpview.py <seq> <fold>

Displays  folding <fold> of sequence  <seq> in the  2D HP model, where
<seq> is a string over the  alphabet {h,p} and  <fold> is a folding of
<seq> in either relative or absolute format. The length of <fold> must
be exactly one less than the length of <seq>.

A folding in    relative format is   a sequence  over  {f,l,r},  which
describes  the fold  as a sequence  of  steps  (f)orward, (l)left,  or
(r)ight.

A folding  in  absolute format  is  a  sequence  over {n,s,e,w}, which
describes the  fold as a sequence of   steps to the  (n)orth, (s)outh,
(e)east, or (w)est.              
"""
    )


#####################################################################
# Main
#####################################################################

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print()
        print("Wrong number of arguments.")
        print_usage()
        sys.exit(1)

    seq = HPFold(sys.argv[1])

    if len(seq) != len(sys.argv[1]):
        print()
        print("The sequence %s contains illegal characters." % (sys.argv[1]))
        print_usage()
        sys.exit(1)

    absfold = make_absfold(sys.argv[2])
    relfold = make_relfold(sys.argv[2])

    if len(absfold) != len(sys.argv[2]) and len(relfold) != len(sys.argv[2]):
        print()
        print("The folding %s contains illegal characters." % (sys.argv[2]))
        sys.exit(1)

    if len(absfold) == len(seq) - 1:
        seq.SetAbsFold(absfold)
    elif len(relfold) == len(seq) - 1:
        seq.SetRelFold(relfold)
    else:
        print()
        print("The folding %s has wrong length." % (sys.argv[2]))
        print_usage()
        sys.exit(1)

    seq.PrintFold()
