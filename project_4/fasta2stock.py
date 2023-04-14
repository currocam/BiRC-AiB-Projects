import sys
from Bio import AlignIO
infile = sys.argv[1]
align = AlignIO.read(infile, 'fasta')
print(format(align, "stockholm"))