FILES="tests/testseqs/*"
for f in $FILES
do
  echo "Processing $f file..."
  echo $(pwd)
  # take action on each file. $f store current file name
  python benchmark/benchmark_approx.py $f >>  benchmark/benchmark_approx.csv
  python benchmark/benchmark_exact.py $f >>  benchmark/benchmark_exact.csv
done