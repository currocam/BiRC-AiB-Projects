#!/bin/bash
mkdir tmp

echo "algo,length,real,user,sys" > benchmark/benchmark.tsv
# Basic range in for loop
for value in {0..500..20}
do
echo $value
# Create random files
python benchmark/simulate_fasta.py $value $value
    for _ in {1..3}
    do
    /usr/bin/time -f "global-linear_alignment,$value,%E,%U,%S" --append -o benchmark/benchmark.tsv \
        python main.py global-linear tmp/temp_0.fasta \
        tmp/temp_1.fasta tests/case1/file.conf --print-alignment >/dev/null
    /usr/bin/time -f "global-linear,$value,%E,%U,%S" --append -o benchmark/benchmark.tsv \
        python main.py global-linear tmp/temp_0.fasta \
        tmp/temp_1.fasta tests/case1/file.conf >/dev/null
    /usr/bin/time -f "global-linear-linspace,$value,%E,%U,%S" --append -o benchmark/benchmark.tsv \
        python main.py global-linear-linspace tmp/temp_0.fasta \
        tmp/temp_1.fasta tests/case1/file.conf >/dev/null
    done
done
rm -r tmp