

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