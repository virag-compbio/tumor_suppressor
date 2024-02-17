import sys, os

def file_to_list(input_file):

    with open(input_file, 'r') as FI:
        assemblies_list = FI.readlines()
    assemblies_list = [assembly.rstrip('\n') for assembly in assemblies_list]
    return assemblies_list

def get_edit_distance(assembly_1, assembly_2):
    ## from https://www.javatpoint.com/edit-distance-in-python
    
    m, n = len(assembly_1), len(assembly_2)  
    dp = [[0] * (n + 1) for _ in range(m + 1)]  
    for i in range(m + 1):  
        for j in range(n + 1):  
            if i == 0:  
                dp[i][j] = j  
            elif j == 0:  
                dp[i][j] = i  
            elif assembly_1[i - 1] == assembly_2[j - 1]:  
                dp[i][j] = dp[i - 1][j - 1]  
            else:  
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])  
  
    return dp[m][n]  

if __name__ == '__main__':

    shared_assemblies = sys.argv[1]
    assemblies_120way = sys.argv[2]
    assemblies_toga   = sys.argv[3]

    shared_assemblies_list = file_to_list(shared_assemblies)
    assemblies_120way_list = file_to_list(assemblies_120way)
    assemblies_toga        = file_to_list(assemblies_toga)

    for assembly in assemblies_120way_list:
        if assembly not in shared_assemblies_list:

            pot_match = list()
            for ass_toga in assemblies_toga:
                if get_edit_distance(assembly, ass_toga) <= 3:
                    pot_match.append(ass_toga)

            pot_match_string = ','.join(pot_match)
            print(f'{assembly}\t{pot_match_string}')
        else:
            print(f'{assembly}\t{assembly}\tResolved') 

