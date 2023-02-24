# First case
python main.py global-linear tests/case1/seq1.fasta \
    tests/case1/seq2.fasta tests/case1/file.conf --print-alignment -o tmp.fasta
bash tests/scripts/cmp.sh tmp.fasta tests/expected/case1.fasta
rm tmp.fasta


python main.py global-linear tests/case1/seq1.fasta \
    tests/case1/seq2.fasta tests/case1/file.conf -o tmp.fasta
head -n 1 tests/expected/case1.fasta > tmp2.txt
bash tests/scripts/cmp.sh tmp.fasta tmp2.txt
rm tmp.fasta tmp2.txt

python main.py global-linear-linspace tests/case1/seq1.fasta \
    tests/case1/seq2.fasta tests/case1/file.conf -o tmp.fasta
head -n 1 tests/expected/case1.fasta > tmp2.txt
bash tests/scripts/cmp.sh tmp.fasta tmp2.txt
rm tmp.fasta tmp2.txt

python main.py global-affine tests/case1/seq1.fasta \
    tests/case1/seq2.fasta tests/case1/affine.conf -o tmp.fasta
head -n 1 tests/expected/case1_affine.fasta > tmp2.txt
bash tests/scripts/cmp.sh tmp.fasta tmp2.txt
rm tmp.fasta tmp2.txt

# Second case
python main.py global-linear tests/case2/seq1.fasta \
    tests/case2/seq2.fasta tests/case2/file.conf --print-alignment -o tmp.fasta
bash tests/scripts/cmp.sh tmp.fasta tests/expected/case2.fasta
rm tmp.fasta

python main.py global-linear tests/case2/seq1.fasta \
    tests/case2/seq2.fasta tests/case2/file.conf -o tmp.fasta
head -n 1 tests/expected/case2.fasta > tmp2.txt
bash tests/scripts/cmp.sh tmp.fasta tmp2.txt
rm tmp.fasta tmp2.txt

python main.py global-linear-linspace tests/case2/seq1.fasta \
    tests/case2/seq2.fasta tests/case2/file.conf -o tmp.fasta
head -n 1 tests/expected/case2.fasta > tmp2.txt
bash tests/scripts/cmp.sh tmp.fasta tmp2.txt
rm tmp.fasta tmp2.txt

python main.py global-affine tests/case2/seq1.fasta \
    tests/case2/seq2.fasta tests/case2/affine.conf -o tmp.fasta
head -n 1 tests/expected/case2_affine.fasta > tmp2.txt
bash tests/scripts/cmp.sh tmp.fasta tmp2.txt
rm tmp.fasta tmp2.txt

# Third case
python main.py global-linear tests/case3/seq1.fasta \
    tests/case3/seq2.fasta tests/case3/file.conf --print-alignment -o tmp.fasta
bash tests/scripts/cmp.sh tmp.fasta tests/expected/case3.fasta
rm tmp.fasta

python main.py global-linear tests/case3/seq1.fasta \
    tests/case3/seq2.fasta tests/case3/file.conf -o tmp.fasta
head -n 1 tests/expected/case3.fasta > tmp2.txt
bash tests/scripts/cmp.sh tmp.fasta tmp2.txt
rm tmp.fasta tmp2.txt

python main.py global-linear-linspace tests/case3/seq1.fasta \
    tests/case3/seq2.fasta tests/case3/file.conf -o tmp.fasta
head -n 1 tests/expected/case3.fasta > tmp2.txt
bash tests/scripts/cmp.sh tmp.fasta tmp2.txt
rm tmp.fasta tmp2.txt

python main.py global-affine tests/case3/seq1.fasta \
    tests/case3/seq2.fasta tests/case3/affine.conf -o tmp.fasta
head -n 1 tests/expected/case3_affine.fasta > tmp2.txt
bash tests/scripts/cmp.sh tmp.fasta tmp2.txt
rm tmp.fasta tmp2.txt

#Fourth case (too many alignments)
python main.py global-linear tests/case4/seq1.fasta \
    tests/case4/seq2.fasta tests/case4/file.conf -o tmp.fasta
bash tests/scripts/cmp.sh tmp.fasta tests/expected/case4.fasta
rm tmp.fasta

python main.py global-linear-linspace tests/case4/seq1.fasta \
    tests/case4/seq2.fasta tests/case4/file.conf -o tmp.fasta
bash tests/scripts/cmp.sh tmp.fasta tests/expected/case4.fasta
rm tmp.fasta

python main.py global-affine tests/case4/seq1.fasta \
    tests/case4/seq2.fasta tests/case4/affine.conf -o tmp.fasta
bash tests/scripts/cmp.sh tmp.fasta tests/expected/case4_affine.fasta
rm tmp.fasta