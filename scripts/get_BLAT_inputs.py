import sys
from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq

def fasta_to_dict(fasta_file):
    ''' Reads a FASTA file, stores sequences in a dictionary, and translates nucleotide sequences to protein sequences. '''
    fasta_file = Path(fasta_file)
    assert fasta_file.is_file(), f"Aborting: The FASTA file '{fasta_file}' could not be found."

    fasta_dict = {}
    
    for record in SeqIO.parse(fasta_file, "fasta"):
        seq_id = record.id.split('\t')[0]  # Extract ID before tab, if present
        nt_seq = str(record.seq).replace('-', '')  # Remove gaps
        nt_seq = nt_seq.rstrip('NNN')  # Trim trailing 'NNN' if present
        fasta_dict[seq_id] = str(Seq(nt_seq).translate())

    return fasta_dict

def process_assemblies(assemblies_list, pten_fasta, tp53_fasta, output_file):
    ''' Processes assembly mappings and writes corresponding protein sequences. '''
    pten_fasta_dict = fasta_to_dict(pten_fasta)
    tp53_fasta_dict = fasta_to_dict(tp53_fasta)

    with open(assemblies_list, 'r') as fi, open(output_file, 'w') as fo:
        for line in fi:
            assembly_120way, assembly_toga = line.strip().split('\t')
            toga_key = f"vs_{assembly_toga}"

            tp53_seq = tp53_fasta_dict.get(toga_key, '-')
            pten_seq = pten_fasta_dict.get(toga_key, '-')

            fo.write(f"{assembly_120way}\t{assembly_toga}\t{tp53_seq}\t{pten_seq}\n")

if __name__ == '__main__':
    assemblies_list = sys.argv[1]
    pten_fasta = sys.argv[2]
    tp53_fasta = sys.argv[3]
    output_file = sys.argv[4]

    process_assemblies(assemblies_list, pten_fasta, tp53_fasta, output_file)
