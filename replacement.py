import sys
import json
import math
import pandas as pd
import numpy as np
import sympy
import random
import struct
import re
import heapq
from AAI_experiments_SPN import modify_circuit_replacement_spn
def main(dataset,p,s,method):

    results_dict_replacement = {}
    numerical_loss_before, numerical_loss_after, actual_percentage,normalization_constant = modify_circuit_replacement_spn(dataset, p,s,method)
    if isinstance(numerical_loss_before, np.float128):
        numerical_loss_before = float(numerical_loss_before)
    if isinstance(numerical_loss_after, np.float128):
        numerical_loss_after = float(numerical_loss_after)
    if isinstance(actual_percentage, np.float128):
        actual_percentage = float(actual_percentage)
    if isinstance(normalization_constant, np.float128):
        normalization_constant = float(normalization_constant)
    key = f"{dataset}_{p}_{s}_{method}"
    results_dict_replacement[key] = {
        'numerical_loss_before': numerical_loss_before,
        'numerical_loss_after': numerical_loss_after,
        'actual_percentage': actual_percentage,
        'normalization_constant': normalization_constant
    }
    with open(f'./results/results_replacement_{key}.txt', 'w') as outfile:
        json.dump(results_dict_replacement, outfile, indent=4)






if __name__ == '__main__':

    # Parse command line arguments
    dataset = sys.argv[1]
    p = sys.argv[2]
    s = sys.argv[3]
    method = sys.argv[4]
    main(dataset, p,s,method)
'''
    numerical_loss, actual_percentage=modify_circuit_replacement_spn('book',1,'random', 'nondet')
    print(numerical_loss)
    print(actual_percentage)   


'''
