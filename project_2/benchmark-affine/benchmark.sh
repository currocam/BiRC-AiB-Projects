#!/bin/bash
mkdir tmp

echo "algo,length,real,user,sys" > benchmark-affine/benchmark.tsv
# Basic range in for loop
for value in {0..500..20}
do
echo $value
# Create random files
python benchmark-affine/simulate_fasta.py $value $value
    for _ in {1..3}
    do
    /usr/bin/time -f "global-affine_alignment,$value,%E,%U,%S" --append -o benchmark-affine/benchmark.tsv \
        python main.py global-affine tmp/temp_0.fasta \
        tmp/temp_1.fasta tests/case1/affine.conf --print-alignment >/dev/null
    /usr/bin/time -f "global-affine,$value,%E,%U,%S" --append -o benchmark-affine/benchmark.tsv \
        python main.py global-affine tmp/temp_0.fasta \
        tmp/temp_1.fasta tests/case1/affine.conf >/dev/null
#    /usr/bin/time -f "global-affine-linspace,$value,%E,%U,%S" --append -o benchmark-affine/benchmark.tsv \
#        python main.py global-affine-linspace tmp/temp_0.fasta \
#        tmp/temp_1.fasta tests/case1/affine.conf >/dev/null
    done
done
rm -r tmp