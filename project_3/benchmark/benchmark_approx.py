from memory_profiler import profile
import numpy as np
from typing import Tuple, Optional
import itertools
from Bio import SeqIO, SeqRecord, Seq
import Bio
from dataclasses import dataclass
import sys



SCORE_MATRIX = np.matrix(
    [[0, 5, 2, 5, 5],  # A
    [5, 0, 5, 2, 5],  # C
    [2, 5, 0, 5, 5],  # G
    [5, 2, 5, 0, 5],  # T
    [5, 5, 5, 5, 0]]  #-'
    )
GAP_CHAR = 4
ALPHABET = alphabet = {'A': 0, 'C': 1, 'G': 2, 'T': 3, '-': 4}
def dna2int(x: str)-> list[int]:
    '''
    >>> dna2int('ACGT-A')
    [0, 1, 2, 3, 4, 0]
    '''
    return list(alphabet.get(char) for char in x)
def int2dna(x: list[int])-> str:
    '''
    >>> int2dna([0, 1, 2, 3, 4, 0])
    'ACGT-A'
    '''
    collapsed = "".join(ALPHABET)
    return "".join(collapsed[i] for i in x)

def score_sum_pairs(*chars: Optional[int])-> int:
    """
    >>> score_sum_pairs(0, 0, 0)
    0
    >>> score_sum_pairs(0, 1, 2)
    12
    >>> score_sum_pairs(0, 1)
    5
    """
    return sum(SCORE_MATRIX[x, y] for x, y in itertools.combinations(chars, 2))

@dataclass
class MSA:
    cost: int
    sequences: tuple[str]

def get_plausible_path(index):
    """This function computes all possible combinations for a given index 
    assuming a global alignment. It' 1-indexed, so 0 means gap. 
    >>> get_plausible_path((0, 0, 0))
    set()
    >>> get_plausible_path((22, 1, 10))
    {(0, 0, 10), (0, 1, 10), (0, 1, 0), (22, 1, 10), (22, 0, 10), (22, 0, 0), (22, 1, 0)}
    """
    gaps_over_gaps = tuple(0 for _ in index)
    all_combs = np.array(list(itertools.product([0, 1], repeat=len(index))))
    return set(tuple(index * comb) for comb in all_combs if tuple(index * comb) != gaps_over_gaps)
def get_previous_index(index, comb):
    """This function gets the previous index for a given combination and index
    The combination it's 1-indexed in reference to the sequence
    >>> get_previous_index((1, 1, 1), (1, 1, 1))
    (0, 0, 0)
    >>> get_previous_index((15, 12, 1), (1, 0, 1))
    (14, 12, 0)
    """
    return tuple(i - 1 if v else i for i, v in zip(index, comb))

def compute_exact_alignment(*seq)-> np.ndarray:
    """
    >>> compute_exact_alignment("")[-1]
    0
    >>> compute_exact_alignment("", "", "")[-1, -1, -1]
    0
    >>> compute_exact_alignment("ACGTGTCAACGT", "ACGTCGTAGCTA")[-1, -1]
    22
    >>> compute_exact_alignment("AATAAT", "AAGG")[-1, -1]
    14
    """
    sequences: Tuple[int] = tuple(dna2int(x) for x in seq)
    shapes = tuple(len(x)+1 for x in sequences)
    D = np.zeros(shapes, dtype = "int")
    for index in np.ndindex(D.shape):
        possibilities = set()
        for direction in get_plausible_path(index):
            previous_cost = D[get_previous_index(index, direction)]
            extension_cost = score_sum_pairs(
                *[sequence[v-1] if v else GAP_CHAR for v, sequence in zip(direction, sequences)]
            )
            possibilities.add(previous_cost + extension_cost)
        if possibilities:
            D[index] = min(possibilities)    
    return D

def linear_backtrack(D: np.ndarray, *seq):
    """Compute alignment in linear time using the whole cost matrix"""
    sequences: Tuple[int] = tuple(dna2int(x) for x in seq)
    alignment = np.empty((len(sequences), 0), dtype = "int")
    indexes = tuple(elm -1 for elm in D.shape)
    while sum(indexes) != 0:
        for comb in get_plausible_path(indexes):
            previous_pos = get_previous_index(indexes, comb)
            new_aligned_col = [sequence[v-1] if v else GAP_CHAR for v, sequence in zip(comb, sequences)]
            if D[indexes] == D[previous_pos] + score_sum_pairs(*new_aligned_col):
                alignment = np.column_stack((alignment, np.array(new_aligned_col)))
                indexes = previous_pos
                break
    return tuple(int2dna(seq.tolist()) for seq in np.flip(alignment,axis = 1))

def global_alignment(*sequences) -> MSA:
    """
    Compute an optimal global alignment of 3 sequences
    >>> global_alignment("")
    MSA(cost=0, sequences=('',))
    >>> global_alignment("", "")
    MSA(cost=0, sequences=('', ''))
    >>> global_alignment("A", "")
    MSA(cost=5, sequences=('A', '-'))
    >>> global_alignment("AATAAT", "AAGG")
    MSA(cost=14, sequences=('AATAAT', 'AA-GG-'))
    >>> global_alignment("A", "", "C", "GG", "AA", "C")
    MSA(cost=101, sequences=('-A', '--', '-C', 'GG', 'AA', '-C'))
    >>> global_alignment("GTTCCGAAAGGCTAGCGCTAGGCGCC", "ATGGATTTATCTGCTCTTCG", "TGCATGCTGAAACTTCTCAACCA")
    MSA(cost=198, sequences=('GTTCCGAAAGGCTAGCGCTAGGC-GCC-', 'AT---GGAT--TT-AT-CTGCTC-TTCG', '-T---GCATG-CTGAAACTTCTCAACCA'))
    """
    D = compute_exact_alignment(*sequences)
    return MSA(
        D[tuple(i-1 for i in D.shape)],
        linear_backtrack(D, *sequences)
        )

def find_first_sequence(sequences: [str])-> int:
    """
    Finds the first sequence for 2-approximation algorithm
    >>> find_first_sequence(["AA", "CT", "CT"])
    1
    """
    n = len(sequences)
    shape = (n, n)
    pairwises = np.zeros(shape,dtype="int")
    for i, j in zip(*np.triu_indices(n,k=1, m=n)):
        pairwises[i, j] = pairwises[j, i] = global_alignment(sequences[i], sequences[j]).cost
    return np.argmin([sum(row) for row in pairwises])   

def extend_MSA(M: np.ndarray , A: MSA) -> np.ndarray:
    """
    Extend a MSA with a given pairwise alignment. 
    >>> x = np.array([['A', 'C'],['A', '-']])
    >>> y = global_alignment("AC", "GC")
    >>> extend_MSA(x, y)
    array([['A', 'C'],
           ['A', '-'],
           ['G', 'C']], dtype='<U1')
    """
    A = A.sequences
    new_msa = np.empty((M.shape[0]+1, 0), dtype = "<U1")
    i, j = 0, 0
    while i < M.shape[1] and j < len(A[0]):
        if M[0, i] == A[0][j]:
            new_column =  np.append(M[:, i], A[1][j])
            new_column = new_column.reshape((len(new_column),1))
            new_msa = np.hstack((new_column, new_msa))
            i+=1
            j+=1
        elif M[0, i] == "-":
            new_column =  np.append(M[:, i], "-")
            new_column = new_column.reshape((len(new_column),1))
            new_msa = np.hstack((new_column, new_msa))
            i+=1
        elif A[0][j] == "-":
            new_column =  np.append(M.shape[0]*["-"], A[1][j])
            new_column = new_column.reshape((len(new_column),1))
            new_msa = np.hstack((new_column, new_msa))
            j+=1
    while i < M.shape[1]:
        new_column =  np.append(M[:, i], "-")
        new_column = new_column.reshape((len(new_column),1))
        new_msa = np.hstack((new_column, new_msa))
        i+=1
    while j < len(A[0]):
        new_column =  np.append(M.shape[0]*["-"], A[1][j])
        new_column = new_column.reshape((len(new_column),1))
        new_msa = np.hstack((new_column, new_msa))
        j+=1
    return  np.flip(new_msa, 1)

def compute_2P_approximation(*sequences)-> np.ndarray:
    first = find_first_sequence(sequences)
    alignments = list()
    for second, _ in enumerate(sequences):
        if second != first:
            alignments.append(global_alignment(sequences[first], sequences[second]))
    MultipleAligment = np.array([ list(seq) for seq in alignments.pop().sequences]) 
    while alignments:
        pairwise = alignments.pop()
        MultipleAligment = extend_MSA(MultipleAligment, pairwise)
    cost = sum(score_sum_pairs(*[dna2int(char) for char in col]) for col in MultipleAligment.T)
    aligned_sequences = tuple("".join(x) for x in MultipleAligment)
    return MSA(cost = int(cost), sequences = aligned_sequences)
  
if __name__=='__main__':
    import time
    import psutil

    start_time = time.time()
    process = psutil.Process()
    
    infile = sys.argv[1]
    sequences = [str(x.seq) for x in SeqIO.parse(infile,'fasta')]
    approximate_cost = compute_2P_approximation(*sequences).cost
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    memory_usage = process.memory_info().rss / 1024 / 1024
    print(f"{infile},{elapsed_time},{memory_usage}")