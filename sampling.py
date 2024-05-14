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
from AAI_experiments_SPN import sampling_spn
def main(dataset):
    sampling_spn(str(dataset), str(dataset)+'_all1_input.txt')





if __name__ == '__main__':

    # Parse command line arguments
    dataset = sys.argv[1]
    #dataset = 'nltcs'
    main(dataset)
