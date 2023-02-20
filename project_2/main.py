from typing import Sized, Tuple, Optional
import typer
from Bio import SeqIO
from pathlib import Path
import numpy as np
import sys
from dataclasses import dataclass
from Bio.Seq import Seq

# Helper dataclass and fn

def construct_alphabet(x: str) -> dict[str: int]:
    return {char:index for index, char in enumerate(x)}

@dataclass
class ConfigurationAlignment:
    """Class for keeping alignment specification."""
    gap_cost: int
    alphabet: dict[str: int]
    score_matrix: np.ndarray

@dataclass
class CostMatrix:
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
    dyn_mat = CostMatrix(np.empty(dim, dtype=int))
    # Define C function
    def C(i: int, j: int)-> int:
        match i:
            case 0 if j == 0: return 0
            case _ if j == 0: return i * conf.gap_cost
            case 0 if j != 0: return j * conf.gap_cost
        return np.min([
            dyn_mat.get_value(i-1, j) + conf.gap_cost,
            dyn_mat.get_value(i, j-1) + conf.gap_cost,
            dyn_mat.get_value(i-1, j-1) + conf.score_matrix[x[i-1], y[j-1]]
            ])

    for i in range(len(x)+1):
        for j in range(len(y)+1):
            dyn_mat.set_value(C(i, j),i, j)
    return dyn_mat

def global_affine_matrix(
    x: list[int], y: list[int], conf: ConfigurationAlignment,
    linspace = False) -> np.ndarray:
    """Fill global linear matrix for minimize problem"""
    # Init empty matrix
    dim = (len(x)+1, len(y)+1) if not linspace else (2, len(y)+1)
    dyn_mat = CostMatrix(np.empty(dim, dtype=int))
    raise NotImplemented

def back_tracking_matrix(
    i: int, j: int, T: np.ndarray,
    A: list[int], B: list[int], conf: ConfigurationAlignment,
    aligned_1 = None, aligned_2 = None
    )-> Tuple[list[int], list[int]]:
    """Compute alignment in linear time using the whole cost matrix"""
    aligned_1, aligned_2 = list(), list()
    while i != 0 and j != 0:
        if (i > 0) and (j > 0) and T[i,j] == T[i-1, j-1] +  conf.score_matrix[A[i-1], B[j-1]]:
            aligned_1.append(A[i-1])
            aligned_2.append(B[j-1])
            i -= 1
            j -= 1
        if (i > 0) and (j >= 0) and T[i,j] == T[i-1,j] + conf.gap_cost:
            aligned_1.append(A[i-1])
            aligned_2.append(conf.alphabet["-"])
            i -= 1
        if (i>=0) and (j > 0) and T[i,j] == T[i,j-1] + conf.gap_cost:
            aligned_1.append(conf.alphabet["-"])
            aligned_2.append(B[j-1])
            j -= 1
    return (reversed(aligned_1), reversed(aligned_2))

# CLI app

app = typer.Typer()

def read_configuration_file(file: Path) -> ConfigurationAlignment:
    "Read configuration file"
    with file.open() as f:
        lines = [line.rstrip('\n') for line in f]
        gap_cost = int(lines[0])
        parsing = dict()
        for line in lines[1:]:
            chars = line.split()
            parsing[chars[0]] = [int(x) for x in chars[1:]]
        alphabet = construct_alphabet("".join(parsing.keys()) + "-")
        score_matrix = np.matrix(list(parsing.values()))
        return ConfigurationAlignment(gap_cost, alphabet, score_matrix)

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
        aligned_1, aligned_2 = back_tracking_matrix(len(x), len(y), mat.mat, *args)
        seq1.seq, seq2.seq  = Seq(int2dna(aligned_1)), Seq(int2dna(aligned_2))
        SeqIO.write(iter([seq1, seq2]), f, "fasta")

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
    mat = global_affine_matrix(*args)
    print(f"; The optimal cost of this alignment is {mat.get_value(len(x), len(y))}", file = f)
    if print_alignment:
        aligned_1, aligned_2 = back_tracking_matrix(len(x), len(y), mat.mat, *args)
        seq1.seq, seq2.seq  = Seq(int2dna(aligned_1)), Seq(int2dna(aligned_2))
        SeqIO.write(iter([seq1, seq2]), f, "fasta")

if __name__ == "__main__":
    app()