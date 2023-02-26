

## Set up

``` bash
conda create -n project2 python=3.10 biopython typer numpy
conda activate project2
```

## How to run

To see available programs: 
``` bash
python main.py --help
                                                                                                                      
 Usage: main.py [OPTIONS] COMMAND [ARGS]...                                                                           
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ global-affine           This program finds the cost of a global alignment and, optionally, the  alignment itself   │
│                         in quadratic time and space.                                                               │
│ global-linear           This program finds the cost of a global alignment and, optionally, the  alignment itself   │
│                         in quadratic time and space.                                                               │
│ global-linear-linspace  This program finds the cost of a global alignment quadratic time and  linear space.        │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

Let's inspect global-linear options:

``` bash
python main.py global-affine --help
                                                                                                                      
 Usage: main.py global-affine [OPTIONS] SEQUENCE_1 SEQUENCE_2 CONFIGURATION                                           
                                                                                                                      
 This program finds the cost of a global alignment and, optionally, the  alignment itself in quadratic time and       
 space.                                                                                                               
                                                                                                                      
╭─ Arguments ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    sequence_1         PATH  [default: None] [required]                                                           │
│ *    sequence_2         PATH  [default: None] [required]                                                           │
│ *    configuration      PATH  [default: None] [required]                                                           │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --print-alignment                                                                                                  │
│ --outfile          -o      PATH  [default: None]                                                                   │
│ --help                           Show this message and exit.                                                       │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

If we try to run without enough arguments, it will fail:

``` bash
 python main.py global-affine seq1.fasta seq2.fasta
Usage: main.py global-affine [OPTIONS] SEQUENCE_1 SEQUENCE_2 CONFIGURATION
Try 'main.py global-affine --help' for help.
╭─ Error ────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Missing argument 'CONFIGURATION'.                                                                                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

We can find the optimal cost and an alignment for linear and affine gap cost. We can either print to standard output or to file. For printing the optimal cost, we are using the fact that ";" is the comment keyword for fasta files. 

``` bash
python main.py global-linear seq1.fasta seq2.fasta linear.conf --print-alignment
```

We can also find the optimal cost using only linear space:

``` bash
python main.py global-linear-linspace seq1.fasta seq2.fasta linear.conf -o output.fasta
```

## How to run tests

``` bash
bash tests/run_test.sh
```

# How to benchmark

``` bash
bash benchmark/benchmark.sh
```

## Evaluation

Question 1 
---------- 

Compute the score of an optimal alignment and an optimal alignment of
seq1 and seq2 above using the programs global_linear using the above
score matrix M and gap cost g(k)=5*k

``` bash
python main.py global-linear results/seq1.fasta results/seq2.fasta results/global-linear.conf --print-alignment

; The optimal cost of this alignment is 226
>seq1
TATGGA-GAGAATAAAAGAACTGAGAGATCTAATG-TCGCAGTCCCGCAC-TCGCGAGAT
ACT-CACTAAGAC-CACTGTGGACCATATGGCCATAATCAAAAAG
>seq2
-ATGGATGTCAATCCGACT-CTACTTTTCCTAAAAATTCCAGCGCAAAATGCCATAAG-C
ACCACATTCCCTTATACTGGAGATCCTCCA-T-ACAGCCATGGAA
```

Question 2
----------

Compute the score of an optimal alignment and an optimal alignment of
seq1 and seq2 above using the program global_affine using the above
score matrix M and gap cost g(k)=5+5*k

``` bash
python main.py global-affine results/seq1.fasta results/seq2.fasta results/global-affine.conf --print-alignment

; The optimal cost of this alignment is 266
>seq1
TATGGAGAGAATAAAAGAACTGAGAGATCTAATG-TCGCAGTCCCGCACTCGCGAGATAC
T-CACTAAGAC-CACTGTGGACCATATGGCCATAATCAAAAAG
>seq2
-ATGGATGTCAATCCGACTCTACTTTTCCTAAAAATTCCAGCGCAAAATGCCATAAGCAC
CCCATTCCCTTTTACTGGAGATCCTCCA--TACAGCCATGGAA
```

Question 3
----------

Compute the optimal score of an optimal alignment for each pair of the
5 sequences above using global_linear with the score matrix M and gap
cost g(k)=5*k. The result is a 5x5 table where entry (i,j) the optimal
score of an alignment of seqi and seqj.


``` bash
python main.py pairwise-global-linear results/sequences.fasta results/global-linear.conf

0 226 206 202 209
226 0 239 223 220
206 239 0 219 205
202 223 219 0 210
209 220 205 210 0
```

Question 4
----------

Compute the optimal score of an optimal alignment for each pair of the
5 sequences above using global_affine with the score matrix M and gap
cost g(k)=5+5*k. The result is a 5x5 table where entry (i,j) the
optimal score of an alignment of seqi and seqj.

``` bash
python main.py pairwise-global-affine results/sequences.fasta results/global-affine.conf

0 266 242 243 256
266 0 283 259 254
242 283 0 269 243
243 259 269 0 247
256 254 243 247 0
```