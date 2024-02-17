import sys, os, subprocess
from urllib.request import urlretrieve
import argparse

def run_subprocess(command):
    command_list = command.split()
    command_return = subprocess.run(command_list, capture_output = True, text = True)
    return command_return

def create_temp_devshm():
    command = 'mktemp /dev/shm/XXXXX'
    command_return = subprocess.run(command.split(), capture_output = True, text = True)
    return command_return.stdout.rstrip('\n')        

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "BLAT pipeline to find out if a gene of interest is present in more than one copies in a genome")
    parser.add_argument("input", help = 'input file', type = str)
    parser.add_argument("output", help = 'output directory', type = str)
    parser.add_argument("log", help = 'log file', type = str)
    parser.add_argument("-keep_2bit", help = 'Keep the two bit files that are downloaded', action = 'store_true') ## useful for debugging

    args = parser.parse_args()
    input_file  = args.input
    output_dir  = args.output
    log_file    = args.log
    keep_2bit   = args.keep_2bit

    os.makedirs(output_dir, exist_ok = True)
    tmp_fasta = create_temp_devshm()

    with open(input_file, 'r') as FI, open(log_file, 'w') as FOL:
        for line in FI:
            assembly_120way, _, tp53_seq, pten_seq = line.rstrip('\n').split('\t')
            two_bit_file = f'{assembly_120way}.2bit'

            assembly_download_link = f'https://bds.mpi-cbg.de/hillerlab/120MammalAlignment/Human120way/data/Genome2bitFiles/{two_bit_file}'
            urlretrieve(assembly_download_link, two_bit_file) ## download the assembly's 2-bit file

            ## create BLAT input, basically a fasta file
            with open(tmp_fasta, 'w') as FO:
                FO.write(f'>{assembly_120way}_TP53\n{tp53_seq}\n>{assembly_120way}_PTEN\n{pten_seq}\n')

            output_file = os.path.join(output_dir, f'{assembly_120way}.txt')    
            ## run BLAT:
            blat_call = f'blat {two_bit_file} {tmp_fasta} {output_file} -q=prot -t=dnax'
            status_blat = run_subprocess(blat_call)

            if status_blat.returncode != 0:
                FOL.write(f'### Error with running blat ###\t{assembly_120way}\t{status_blat.stdout}\t{status_blat.stderr}\n')
            else:    
                FOL.write(f'### Done!!! BLAT search finished for {assembly_120way}\n')

            ## delete the two bit file that was downloaded
            if not keep_2bit:
                os.remove(two_bit_file)

    os.remove(tmp_fasta)            
