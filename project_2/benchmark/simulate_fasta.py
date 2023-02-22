import random
import string 
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
import sys

# get random string of letters and digits
SOURCE = string.ascii_letters + string.digits
ALPHABET = "ACGT"
def generate_random_fasta(n: int)-> SeqRecord:
    return SeqRecord(
    Seq(''.join((random.choice(ALPHABET) for i in range(n)))),
    id= ''.join((random.choice(SOURCE) for i in range(8))),
    name="",
    description="",
)

if __name__ == "__main__":
    for i, n in enumerate(sys.argv[1:]):
        SeqIO.write(generate_random_fasta(int(n)), f"tmp/temp_{i}.fasta", format = "fasta")
    
    
