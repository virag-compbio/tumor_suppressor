import sys, os
from Bio.Seq import Seq

def fasta_to_dict(fasta_file):
    ''' Read the fasta file, convert it to a dict and then translate the nucleotide sequences to protein sequences '''

    assert os.path.isfile(fasta_file), f'Aborting, the fasta file {fasta_file} could not be found'
    fasta_file_dict = dict()
    seq, seq_id = '', ''

    with open(fasta_file, 'r') as FI:
        for line in FI:
            line = line.rstrip('\n')
            if line.startswith('>'):
                if seq != '':
                    fasta_file_dict[seq_id] = seq
                    seq, seq_id = '', ''
                seq_id_list = line.split('\t')
                seq_id = seq_id_list[0].lstrip('>')
            else:
                seq += line
    fasta_file_dict[seq_id] = seq
    
    ## Now the translation business:
    for seq_id, nt_seq in fasta_file_dict.items():
        nt_seq = nt_seq.replace('-','')
        if nt_seq[-3:] == 'NNN':
            nt_seq = nt_seq.rstrip('NNN')
        
        fasta_file_dict[seq_id] = str(Seq(nt_seq).translate())

    return fasta_file_dict

########################################
########################################

if __name__  == '__main__':
    assemblies_list = sys.argv[1]
    pten_fasta      = sys.argv[2]
    tp53_fasta      = sys.argv[3]
    output_file     = sys.argv[4]

    pten_fasta_dict = fasta_to_dict(pten_fasta)
    tp53_fasta_dict = fasta_to_dict(tp53_fasta)   

    with open(assemblies_list, 'r') as FI, open(output_file, 'w') as FO:
        for line in FI:
            assembly_120way, assembly_toga = line.rstrip('\n').split('\t')

            assembly_toga_key = 'vs_' + assembly_toga
            pten_seq = pten_fasta_dict[assembly_toga_key] if assembly_toga_key in pten_fasta_dict else '-'
            tp53_seq = tp53_fasta_dict[assembly_toga_key] if assembly_toga_key in tp53_fasta_dict else '-'

            FO.write(f'{assembly_120way}\t{assembly_toga}\t{tp53_seq}\t{pten_seq}\n')

