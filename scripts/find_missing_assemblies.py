import sys
from pathlib import Path
import argparse

def file_to_list(input_file):
    ''' Read the file to a list '''
    with open(input_file, 'r') as file:
        return [line.rstrip('\n') for line in file]

def get_edit_distance(s1, s2):
    ''' Calculate the edit distance (Levenshtein distance) between two strings '''
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

def main():
    parser = argparse.ArgumentParser(description="Find potential matches for assemblies based on edit distance.")
    parser.add_argument("shared_assemblies", help="File containing shared assemblies", type=str)
    parser.add_argument("assemblies_120way", help="File containing 120-way assemblies", type=str)
    parser.add_argument("assemblies_toga", help="File containing TOGA assemblies", type=str)
    args = parser.parse_args()

    shared_assemblies = file_to_list(args.shared_assemblies)
    assemblies_120way = file_to_list(args.assemblies_120way)
    assemblies_toga = file_to_list(args.assemblies_toga)

    for assembly in assemblies_120way:
        if assembly in shared_assemblies:
            print(f'{assembly}\t{assembly}\tResolved')
        else:
            pot_match = [ass_toga for ass_toga in assemblies_toga if get_edit_distance(assembly, ass_toga) <= 3]
            pot_match_string = ','.join(pot_match)
            print(f'{assembly}\t{pot_match_string}')

if __name__ == '__main__':
    main()