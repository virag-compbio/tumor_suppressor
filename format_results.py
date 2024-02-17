import sys, os, subprocess

def run_subprocess(command):

    command_list = command.split()
    command_return = subprocess.run(command_list, capture_output = True, text = True)
    assert command_return.returncode == 0, f'Aborting, the command {command} could not be completed. Here are the messages\n{command_return.stderr}\n\n{command_return.stdout}\n\n'

def write_results(header, results_list, output_file):

    with open("temp.txt", 'w') as FOR:
        for line in header:
            FOR.write(line)
        for line in results_list:
            FOR.write(line)

    ssconvert_call = f'ssconvert temp.txt {output_file}'
    run_subprocess(ssconvert_call)    


if __name__ == '__main__':

    input_dir   = sys.argv[1]
    output_P53  = sys.argv[2]
    output_PTEN = sys.argv[3]

    os.makedirs(output_P53, exist_ok = True)
    os.makedirs(output_PTEN, exist_ok = True)

    files_list = os.listdir(input_dir)
    for species in files_list:

        input_file = os.path.join(input_dir, species)
        species = species.replace('.txt','')

        with open(input_file, 'r') as FI:
            input_file_list = FI.readlines()

        header = input_file_list[0:5]

        results_p53, results_pten = list(), list()
        for line in input_file_list:
            if 'P53' in line:
                results_p53.append(line)
            elif 'PTEN' in line:
                results_pten.append(line)

        p53_output = os.path.join(output_P53, f'{species}.xlsx')
        pten_output = os.path.join(output_PTEN, f'{species}.xlsx')
        write_results(header, results_p53, p53_output)
        write_results(header, results_pten, pten_output)

