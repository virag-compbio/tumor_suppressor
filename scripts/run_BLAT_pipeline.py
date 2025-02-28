import sys, os
import subprocess
import shlex
import argparse
import logging
from urllib.request import urlretrieve
from pathlib import Path

def run_subprocess(command):
    """Run a subprocess command and return the result."""
    command_list = shlex.split(command)
    result = subprocess.run(command_list, capture_output=True, text=True)
    return result

def create_temp_devshm():
    """Create a temporary file in /dev/shm and return its path."""
    result = subprocess.run(['mktemp', '/dev/shm/XXXXX'], capture_output=True, text=True)
    return result.stdout.rstrip('\n')

def main():
    parser = argparse.ArgumentParser(description="BLAT pipeline to find out if a gene of interest is present in more than one copies in a genome")
    parser.add_argument("input", help="input file", type=str)
    parser.add_argument("output", help="output directory", type=str)
    parser.add_argument("log", help="log file", type=str)
    parser.add_argument("-keep_2bit", help="Keep the two bit files that are downloaded", action="store_true")

    args = parser.parse_args()

    output_dir = Path(args.output)
    log_file = Path(args.log)
    keep_2bit = args.keep_2bit

    output_dir.mkdir(parents=True, exist_ok=True)

    # Set up logging
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    tmp_fasta = create_temp_devshm()

    try:
        with open(args.input, 'r') as input_file:
            for line in input_file:
                assembly_120way, _, tp53_seq, pten_seq = line.rstrip('\n').split('\t')
                two_bit_file = f'{assembly_120way}.2bit'

                assembly_download_link = f'https://bds.mpi-cbg.de/hillerlab/120MammalAlignment/Human120way/data/Genome2bitFiles/{two_bit_file}'
                urlretrieve(assembly_download_link, two_bit_file)

                with open(tmp_fasta, 'w') as fasta_file:
                    fasta_file.write(f'>{assembly_120way}_TP53\n{tp53_seq}\n>{assembly_120way}_PTEN\n{pten_seq}\n')

                output_file = output_dir / f'{assembly_120way}.txt'
                blat_call = f'blat {two_bit_file} {tmp_fasta} {output_file} -q=prot -t=dnax'
                status_blat = run_subprocess(blat_call)

                if status_blat.returncode != 0:
                    logging.error(f'Error with running blat for {assembly_120way}: {status_blat.stdout} {status_blat.stderr}')
                else:
                    logging.info(f'BLAT search finished for {assembly_120way}')

                if not keep_2bit:
                    os.remove(two_bit_file)
    finally:
        os.remove(tmp_fasta)

if __name__ == '__main__':
    main()