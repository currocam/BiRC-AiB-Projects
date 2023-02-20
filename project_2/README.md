

## Set up

``` bash
conda create -n project2 python=3.10 biopython typer numpy
conda activate project2
```

## How to run

To see available programs: 
``` bash
python main.py --help

Commands:
  global-linear           This program finds the cost of a global...
  global-linear-linspace  This program finds the cost of a global...
```

Let's inspect global-linear options:

``` bash
python main.py global-linear --help
python main.py global-linear --help
Usage: main.py global-linear [OPTIONS] SEQUENCE_1 SEQUENCE_2 CONFIGURATION

  This program finds the cost of a global alignment and, optionally, the
  alignment itself in quadratic time and space.

Arguments:
  SEQUENCE_1     [required]
  SEQUENCE_2     [required]
  CONFIGURATION  [required]

Options:
  --print-alignment
  -o, --outfile PATH
  --help              Show this message and exit.
```

If we try to run without enough arguments, it will fail:

``` bash
python main.py --help

Commands:
  global-linear           This program finds the cost of a global...
  global-linear-linspace  This program finds the cost of a global...
```

We can find the optimal cost and the alignment. We can either print to standard output or to file. 

``` bash
python main.py global-linear integration/seq1.fasta integration/seq2.fasta integration/setting.conf --print-alignment
```


We can also find the optimal cost using only linear space:

``` bash
python main.py global-linear-linspace integration/seq1.fasta integration/seq2.fasta integration/setting.conf
```

## How to run tests

``` bash
bash tests/run_test.sh
```

# How to measure time

``` bash
time python main.py global-linear-linspace tests/case4/seq1.fasta tests/case4/seq2.fasta tests/case4/file.conf

real    0m0.487s
user    0m0.410s
sys     0m0.021s
```

``` bash
time python main.py global-linear tests/case4/seq1.fasta tests/case4/seq2.fasta tests/case4/file.conf

real    0m0.558s
user    0m0.475s
sys     0m0.033s
```