import sys
import os
from pathlib import Path
import csv
from openpyxl import Workbook

def write_results(header, results_list, output_file):
    ''' Writes data to an Excel file using openpyxl. '''
    wb = Workbook()
    ws = wb.active

    # Write header
    for row in header:
        ws.append(row)

    # Write results
    for row in results_list:
        ws.append(row)

    wb.save(output_file)

def process_files(input_dir, output_p53, output_pten):
    ''' Processes files in the input directory and writes categorized results to Excel '''
    input_dir = Path(input_dir)
    output_p53 = Path(output_p53)
    output_pten = Path(output_pten)

    output_p53.mkdir(parents=True, exist_ok=True)
    output_pten.mkdir(parents=True, exist_ok=True)

    for input_file in input_dir.glob("*.txt"):
        species = input_file.stem  # Get filename without extension

        with input_file.open('r', newline='') as fi:
            reader = csv.reader(fi, delimiter='\t')  # Adjust delimiter as needed
            data = list(reader)

        header = data[:5]  # Extract header
        results_p53 = [row for row in data if 'P53' in row]
        results_pten = [row for row in data if 'PTEN' in row]

        if results_p53:
            write_results(header, results_p53, output_p53 / f"{species}.xlsx")
        if results_pten:
            write_results(header, results_pten, output_pten / f"{species}.xlsx")

if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_p53 = sys.argv[2]
    output_pten = sys.argv[3]

    process_files(input_dir, output_p53, output_pten)