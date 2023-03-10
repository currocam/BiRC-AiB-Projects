from collections import namedtuple
from itertools import combinations
from typing import Sized, Tuple, Optional
import warnings
import typer
from Bio import SeqIO
from pathlib import Path
import numpy as np
import sys
from dataclasses import dataclass
from Bio.Seq import Seq

warnings.filterwarnings('ignore')


# Helper dataclass and fn
def construct_alphabet(x: str) -> dict[str: int]:
    return {char:index for index, char in enumerate(x)}

LinearGap = namedtuple("LinearGap", ["value"])
AffineGap = namedtuple("AffineGap", ["alpha", "beta"])

@dataclass
class ConfigurationAlignment:
    """Class for keeping alignment specification."""
    gap: "LinearGap|AffineGap"
    alphabet: dict[str: int]
    score_matrix: np.ndarray

def read_configuration_file(file: Path) -> ConfigurationAlignment:
    "Read configuration file"
    with file.open() as f:
        lines = [line.rstrip('\n') for line in f]
        gap_line = lines[0].split()
        gap = AffineGap(int(gap_line[0]), int(gap_line[1])) if len(gap_line) == 2 else LinearGap(int(gap_line[0]))
        parsing = dict()
        for line in lines[1:]:
            chars = line.split()
            parsing[chars[0]] = [int(x) for x in chars[1:]]
        alphabet = construct_alphabet("".join(parsing.keys()) + "-")
        score_matrix = np.matrix(list(parsing.values()))
        return ConfigurationAlignment(gap, alphabet, score_matrix)

@dataclass
class Matrix:
    """Helper class for accessing cost matrix"""
    mat: np.ndarray
    def get_value(self, i: int, j: int) -> int:
        "Getter for matrix"
        return self.mat[i%self.mat.shape[0], j%self.mat.shape[1]]
    def set_value(self,value: int,  i: int, j: int) -> None:
        "Setter for matrix"
        self.mat[i%self.mat.shape[0], j%self.mat.shape[1]] = value


def dna2int(x: str, alphabet_dict = {'A': 0, 'C': 1, 'G': 2, 'T': 3, '-': 4})-> list[int]:
    '''
    >>> dna2int('ACGT-A')
    [0, 1, 2, 3, 4, 0]
    '''
    return list(alphabet_dict.get(char) for char in x.upper())

def int2dna(x: list[int], alphabet = {'A': 0, 'C': 1, 'G': 2, 'T': 3, '-': 4})-> str:
    '''
    >>> int2dna([0, 1, 2, 3, 4, 0])
    'ACGT-A'
    '''
    alphabet = "".join(alphabet)
    return "".join(alphabet[i] for i in x)

## Algorithms

def global_linear_matrix(
    x: list[int], y: list[int], conf: ConfigurationAlignment,
    linspace = False) -> np.ndarray:
    """Fill global linear matrix for minimize problem"""
    # Init empty matrix
    dim = (len(x)+1, len(y)+1) if not linspace else (2, len(y)+1)
    dyn_mat = Matrix(np.empty(dim, dtype=int))
    # Define C function
    def C(i: int, j: int)-> int:
        if i == 0 and j == 0: return 0
        if j == 0:  return i * conf.gap.value
        if i == 0 and j != 0: return j * conf.gap.value
        return np.min([
            dyn_mat.get_value(i-1, j) + conf.gap.value,
            dyn_mat.get_value(i, j-1) + conf.gap.value,
            dyn_mat.get_value(i-1, j-1) + conf.score_matrix[x[i-1], y[j-1]]
            ])
    for i in range(len(x)+1):
        for j in range(len(y)+1):
            dyn_mat.set_value(C(i, j),i, j)
    return dyn_mat

def global_affine_matrix(
    x: list[int], y: list[int], conf: ConfigurationAlignment) -> np.ndarray:
    """Fill global linear matrix for minimize problem"""
    dim = (len(x)+1, len(y)+1)
    alpha, beta = conf.gap.alpha, conf.gap.beta
    T, I, D = Matrix(np.full(dim, np.nan)), Matrix(np.full(dim, np.nan)), Matrix(np.full(dim, np.nan))
    for i in range(len(x)+1):
        for j in range(len(y)+1):
            v1 = v2 = np.nan
            if i > 0 and j >= 0:  v1 = T.get_value(i-1, j) + (alpha + beta)
            if i > 1 and j >= 0:  v2 = D.get_value(i-1, j) + alpha
            D.set_value(np.nanmin([v1, v2]), i, j)
            v1 = v2 = np.nan
            if i >= 0 and j > 0:  v1 = T.get_value(i, j-1) + (alpha+beta)
            if i >= 0 and j > 1:  v2 = I.get_value(i, j-1) + alpha
            I.set_value(np.nanmin([v1, v2]), i, j)
            v1 = v2 = v3 = v4 = np.nan
            if i == 0 and j == 0: v1 = 0
            if i > 0 and j > 0: v2 = T.get_value(i-1, j-1) + conf.score_matrix[x[i-1], y[j-1]]
            if i > 0 and j >= 0: v3 = D.get_value(i, j)
            if i >= 0 and j > 0: v4 = I.get_value(i, j)
            T.set_value(np.nanmin([v1, v2, v3, v4]), i, j)
    return T, I, D

def global_affine_backtrack(
    T: np.ndarray, I: np.ndarray, D: np.ndarray,
    A: list[int], B: list[int], conf: ConfigurationAlignment,
    aligned_1 = None, aligned_2 = None
    )-> Tuple[list[int], list[int]]:
    """Compute alignment in linear time using the whole cost matrix"""
    aligned_1, aligned_2 = list(), list()
    i, j = len(A), len(B)
    while i != 0 and j != 0:
        if T[i, j] == (T[i-1, j-1] + conf.score_matrix[A[i-1], B[j-1]]):
            aligned_1.append(A[i-1])
            aligned_2.append(B[j-1])
            i -= 1
            j -= 1
        if T[i, j] == D[i, j]:
            while D[i, j] == D[i-1, j] + conf.gap.alpha:
                aligned_1.append(A[i-1])
                aligned_2.append(conf.alphabet["-"])
                i -= 1
            aligned_1.append(A[i-1])
            aligned_2.append(conf.alphabet["-"])
            i -= 1
        if T[i, j] == I[i, j]:
            while I[i, j] == I[i, j-1] + conf.gap.alpha:
                aligned_1.append(conf.alphabet["-"])
                aligned_2.append(B[i-1])
                j -= 1
            aligned_1.append(conf.alphabet["-"])
            aligned_2.append(B[i-1])
            j -= 1
    return (int2dna(reversed(aligned_1)), int2dna(reversed(aligned_2)))

def global_linear_backtrack(
    T: np.ndarray,
    A: list[int], B: list[int], conf: ConfigurationAlignment,
    aligned_1 = None, aligned_2 = None
    )-> Tuple[list[int], list[int]]:
    """Compute alignment in linear time using the whole cost matrix"""
    aligned_1, aligned_2 = list(), list()
    i, j = len(A), len(B)
    while i != 0 and j != 0:
        if (i > 0) and (j > 0) and T[i,j] == T[i-1, j-1] +  conf.score_matrix[A[i-1], B[j-1]]:
            aligned_1.append(A[i-1])
            aligned_2.append(B[j-1])
            i -= 1
            j -= 1
        if (i > 0) and (j >= 0) and T[i,j] == T[i-1,j] + conf.gap.value:
            aligned_1.append(A[i-1])
            aligned_2.append(conf.alphabet["-"])
            i -= 1
        if (i>=0) and (j > 0) and T[i,j] == T[i,j-1] + conf.gap.value:
            aligned_1.append(conf.alphabet["-"])
            aligned_2.append(B[j-1])
            j -= 1
    return (int2dna(reversed(aligned_1)), int2dna(reversed(aligned_2)))

# CLI app

app = typer.Typer()

def read_CLI_input(
    sequence_1: Path, sequence_2: Path, configuration: Path, output: Optional[Path]
    ):
    """Helper function for reading input"""
    seq1: SeqIO.SeqRecord = next(SeqIO.parse(sequence_1,'fasta'))
    seq2: SeqIO.SeqRecord = next(SeqIO.parse(sequence_2,'fasta'))
    conf = read_configuration_file(configuration)
    f = output.open("w") if output else sys.stdout
    return (seq1, seq2, conf, f)


@app.command()
def global_linear_linspace(
    sequence_1: Path, sequence_2: Path,
    configuration: Path,
    output: Optional[Path] = typer.Option(None, "--outfile", "-o")
    ):
    """
    This program finds the cost of a global alignment quadratic time and  linear space. 
    """
    seq1, seq2, conf, f = read_CLI_input(sequence_1, sequence_2, configuration, output)
    x, y = dna2int(seq1.seq, conf.alphabet), dna2int(seq2.seq, conf.alphabet)
    mat = global_linear_matrix(x, y, conf, linspace = True)
    print(f"; The optimal cost of this alignment is {mat.get_value(len(x), len(y))}", file = f)

@app.command()
def global_linear(
    sequence_1: Path, sequence_2: Path,
    configuration: Path,
    print_alignment: bool = typer.Option(False, "--print-alignment"),
    output: Optional[Path] = typer.Option(None, "--outfile", "-o")
    ):
    """
    This program finds the cost of a global alignment and, optionally, the 
    alignment itself in quadratic time and space. 
    """
    
    seq1, seq2, conf, f = read_CLI_input(sequence_1, sequence_2, configuration, output)
    x, y = dna2int(seq1.seq, conf.alphabet), dna2int(seq2.seq, conf.alphabet)
    args = [x, y, conf]
    mat = global_linear_matrix(*args)
    print(f"; The optimal cost of this alignment is {mat.get_value(len(x), len(y))}", file = f)
    if print_alignment:
        aligned_1, aligned_2 = global_linear_backtrack(mat.mat, *args)
        seq1.seq, seq2.seq  = Seq(aligned_1), Seq(aligned_2)
        SeqIO.write(iter([seq1, seq2]), f, "fasta")

@app.command()
def pairwise_global_linear(
    sequences: Path,
    configuration: Path,
    output: Optional[Path] = typer.Option("/dev/stdout", "--outfile", "-o")

    ):
    """
    This program finds all pairwise cost for a global linear alignment. 
    """
    conf = read_configuration_file(configuration)
    sequences = [x for x in SeqIO.parse(sequences,'fasta')]
    matrix = np.empty((len(sequences), len(sequences)), dtype = "int")
    for i in range(len(sequences)):
        for j in range(len(sequences)):
            x, y = dna2int(sequences[i].seq, conf.alphabet), dna2int(sequences[j].seq, conf.alphabet)
            matrix[i, j] = global_linear_matrix(x, y, conf).get_value(len(x), len(y))
    np.savetxt(str(output),matrix,fmt='%.0f')

@app.command()
def pairwise_global_affine(
    sequences: Path,
    configuration: Path,
    output: Optional[Path] = typer.Option("/dev/stdout", "--outfile", "-o")
    ):
    """
    This program finds all pairwise cost for a global affine alignment. 
    """
    conf = read_configuration_file(configuration)
    sequences = [x for x in SeqIO.parse(sequences,'fasta')]
    matrix = np.empty((len(sequences), len(sequences)), dtype = "int")
    for i in range(len(sequences)):
        for j in range(len(sequences)):
            x, y = dna2int(sequences[i].seq, conf.alphabet), dna2int(sequences[j].seq, conf.alphabet)
            mat, _, _ = global_affine_matrix(x, y, conf)
            matrix[i, j] = mat.get_value(len(x), len(y))
    np.savetxt(str(output),matrix,fmt='%.0f')



@app.command()
def global_affine(
    sequence_1: Path, sequence_2: Path,
    configuration: Path,
    print_alignment: bool = typer.Option(False, "--print-alignment"),
    output: Optional[Path] = typer.Option(None, "--outfile", "-o")
    ):
    """
    This program finds the cost of a global alignment and, optionally, the 
    alignment itself in quadratic time and space. 
    """
    seq1, seq2, conf, f = read_CLI_input(sequence_1, sequence_2, configuration, output)
    x, y = dna2int(seq1.seq, conf.alphabet), dna2int(seq2.seq, conf.alphabet)
    args = [x, y, conf]
    T, I, D = global_affine_matrix(*args)
    print(f"; The optimal cost of this alignment is {int(T.get_value(len(x), len(y)))}", file = f)
    if print_alignment:
        aligned_1, aligned_2 = global_affine_backtrack(T.mat, I.mat, D.mat, *args)
        seq1.seq, seq2.seq  = Seq(aligned_1), Seq(aligned_2)
        SeqIO.write(iter([seq1, seq2]), f, "fasta")

if __name__ == "__main__":
    app()