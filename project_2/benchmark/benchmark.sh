#!/bin/bash
mkdir tmp
outfile="benchmark/benchmark.csv"
echo "algo,length,real,user,sys" > $outfile
# Basic range in for loop
for value in {0..700..20}
do
echo $value
# Create random files
python benchmark/simulate_fasta.py $value $value
    for _ in {0..3}
    do
    for algo in global-linear global-affine global-linear-linspace
    do 
        /usr/bin/time -f "no_backtrack_$algo,$value,%E,%U,%S" --append -o $outfile \
            python main.py $algo tmp/temp_0.fasta \
            tmp/temp_1.fasta tests/$algo.conf >/dev/null
    done
    for algo in global-linear global-affine
    do 
        /usr/bin/time -f "with_backtrack_$algo,$value,%E,%U,%S" --append -o $outfile \
            python main.py $algo tmp/temp_0.fasta \
            tmp/temp_1.fasta tests/$algo.conf --print-alignment >/dev/null
    done
    done
done
rm -r tmp
