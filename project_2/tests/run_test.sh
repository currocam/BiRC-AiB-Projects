for i in {1..4}
do
for algo in global-linear global-affine
do
echo Testing case $i: for $algo
python main.py $algo --print-alignment tests/case$i/seq1.fasta \
    tests/case$i/seq2.fasta tests/$algo.conf -o tmp.fasta
bash tests/scripts/cmp.sh tmp.fasta tests/expected/$algo\_$i.fasta
rm tmp.fasta
done;
algo="global-linear-linspace"
echo Testing case $i: for $algo
python main.py $algo tests/case$i/seq1.fasta \
     tests/case$i/seq2.fasta tests/$algo.conf -o tmp.fasta
bash tests/scripts/cmp.sh tmp.fasta tests/expected/$algo\_$i.fasta
rm tmp.fasta
done