#!/usr/bin/env python
# coding: utf-8
# %%

# %%
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
#from sklearn.metrics import mean_absolute_error, mean_squared_error
# !pip install ipyparallel


# # Functions for floating value/binary value conversion



def float_to_bin(float_num, exp_width, sig_width):
    
    # Pack the number into a binary string using struct
    # print("float_num is", float_num)
    packed = struct.pack('!d', float_num)
    # print(f"packed: {packed}")
    # Convert the binary string to an integer, then convert that to a binary string
    # The [2:] slices off the '0b' Python adds at the beginning of binary literals
    binary_str = bin(int.from_bytes(packed, byteorder='big'))[2:]
    # print(f"binary_str_1: {binary_str}")
    # Pad the string with 0s at the beginning to make it 64 bits long
    binary_str = binary_str.zfill(64)
    # print(f"binary_str_2: {binary_str}")
    # Slice the string into the sign bit, exponent, and significand
    #sign_bit = binary_str[0]
    # exponent = binary_str[0:8]-127+(2**exp_width-1)
    # print(f"binary_str[0:11]: {binary_str[0:11]}")
    # print(f"int(binary_str[0:11], 2): {int(binary_str[0:11], 2)}")
    # print(f"int(binary_str[0:11], 2) - 1023: {int(binary_str[0:11], 2) - 1023}")
    # print(f"(2**(exp_width-1) - 1): {(2**(exp_width-1) - 1)}")
    if float_num == 0:
        exponent = 0
    else:
        exponent = int(binary_str[0:12], 2) - 1023 + (2**(exp_width-1) - 1)
    # exponent_binary = bin(int.from_bytes(exponent, byteorder='big'))[2:]
    exp_bin = format(exponent, '0{}b'.format(exp_width))
    significand = binary_str[12:12+sig_width]

    
    exp_int = int(exp_bin, 2)
    sig_int = int(significand, 2)
    #print("exp is",exp_int)
    #print("sig is",  (sig_int / (1 << sig_width)))

    

    
    return exp_int, sig_int
#print(float_to_bin(1.5,3, 2))

def bin_to_float(exp, sig, exp_width, sig_width):
    bias = (1 << (exp_width - 1)) - 1
    exponent_result = exp - bias
    # Convert the integer to binary string
    significand_binary = bin(sig)[2:]
    # Convert binary string back to integer (this step seems redundant in Python since we're converting back and forth)
    significand_integer = int(significand_binary, 2)
    # Calculate significand result
    significand_result = 1 + (significand_integer / (1 << sig_width))
    # Compute the final decimal value
    float_num = significand_result * (2 ** exponent_result)
    if exp==0 and sig==0:
        return 0
    else:
        return float_num
#print(float_to_bin(0.015549424399227265,8, 20))


def circular_left_shift(n, shift_amount, bit_width):
    if shift_amount == 0:
        return n
    mask = (1 << bit_width) - 1  # Create a mask with bit_width number of 1s
    # print(f"mask: {bin(mask)[2:]}")
    # overflow = (n << shift_amount) & ~mask
    # print(f"n: {bin(n)[2:]}")
    # print(f"overflow: {bin(overflow)[2:]}")
    # print(f"(n << shift_amount) & mask: {bin((n << shift_amount) & mask)[2:]}")
    # print(f"overflow >> bit_width: {overflow >> bit_width}")
    # print(f"((n << shift_amount) & mask) | (overflow >> bit_width): {((n << shift_amount) & mask) | (overflow >> bit_width)}")
    return ((n << shift_amount) & mask) #| (overflow >> bit_width)

def circular_right_shift(n, shift_amount, bit_width):
    if shift_amount == 0:
        return n
    mask = (1 << bit_width) - 1  # Create a mask with bit_width number of 1s
    # print(f"mask: {bin(mask)[2:]}")
    # overflow = (n >> shift_amount) & mask
    # print(f"overflow: {bin(overflow)[2:]}")
    return ((n >> shift_amount) & mask) #| (overflow << (bit_width - shift_amount))

class RawFloat:
    def __init__(self, expWidth, sigWidth):
        self.expWidth = expWidth
        self.sigWidth = sigWidth
        self.exp = 0
        self.sig = 0


# # Adder

# %%


class AddRawFN:
    def __init__(self, expWidth, sigWidth):
        self.expWidth = expWidth
        self.sigWidth = sigWidth
        self.a = RawFloat(expWidth, sigWidth)
        self.b = RawFloat(expWidth, sigWidth)
        self.rawOut = RawFloat(expWidth, sigWidth)
    def is_zero(self, value):
        return value.exp == 0 and value.sig == 0
    def compute(self):
        a_iszero = self.is_zero(self.a)
        b_iszero = self.is_zero(self.b)
        #print(f"a_iszero: {a_iszero}")
        #print(f"b_iszero: {b_iszero}")
        notNaN_isZeroOut = a_iszero and b_iszero
        #print(f"notNaN_isZeroOut: {notNaN_isZeroOut}")
        sDiffExps = self.a.exp - self.b.exp
        if sDiffExps < 0:
            modNatAlignDist = -sDiffExps
            common_exp = self.b.exp
            small_sig = self.a.sig
            large_sig = self.b.sig
        else:
            modNatAlignDist = sDiffExps
            common_exp = self.a.exp
            small_sig = self.b.sig
            large_sig = self.a.sig
        # print(f"modNatAlignDist: {modNatAlignDist}")
        # pre_shifted_sig = (small_sig << 2) >> modNatAlignDist
        pre_pre_shifted_sig = (0b01 << self.sigWidth*2) | (small_sig << self.sigWidth)
        # pre_shifted_sig = pre_pre_shifted_sig >> modNatAlignDist #circular_right_shift(pre_pre_shifted_sig, modNatAlignDist, (self.sigWidth + 1)*2)
        pre_shifted_sig = circular_right_shift(pre_pre_shifted_sig, modNatAlignDist, (self.sigWidth + 1)*2)
        # print(f"pre_shifted_sig: {pre_shifted_sig}")
        # print(f"pre_pre_shifted_sig: {pre_pre_shifted_sig}")
        shifted_sig = pre_shifted_sig if modNatAlignDist <= self.sigWidth + 1 else 0
        # print(f"shifted_sig: {shifted_sig}")
        large_sig_ext = (0b01 << (self.sigWidth*2) | (large_sig << self.sigWidth))
        # print(f"large_sig_ext: {large_sig_ext}")
        sig_sum = large_sig_ext + shifted_sig
        # print(f"sig_sum: {sig_sum}")
        # print(f"(sig_sum >> (self.sigWidth + 1)*2 - 1) & 1: {(sig_sum >> (self.sigWidth + 1)*2 - 1) & 1}")
        if notNaN_isZeroOut:
            fullrawout_sig = 0
            fullrawout_exp = 0
        elif a_iszero:
            fullrawout_sig = self.b.sig
            fullrawout_exp = self.b.exp
        elif b_iszero:
            fullrawout_sig = self.a.sig
            fullrawout_exp = self.a.exp
        elif (sig_sum >> ((self.sigWidth + 1)*2 - 1)) & 1:
            fullrawout_sig = circular_left_shift(sig_sum, 1, (self.sigWidth + 1) * 2)
            fullrawout_exp = common_exp + 1
        else:
            fullrawout_sig = circular_left_shift(sig_sum, 2, (self.sigWidth + 1) * 2)
            fullrawout_exp = common_exp
        #print(f"fullrawout_sig: {fullrawout_sig}")
        #print(f"fullrawout_exp: {fullrawout_exp}")
        # Rounding logic
        guardBit = (fullrawout_sig >> (self.sigWidth + 1 )) & 1
        roundBit = (fullrawout_sig >> (self.sigWidth)) & 1
        stickyBit = fullrawout_sig & ((1 << self.sigWidth) - 1) != 0
        leastSigBitOfResult = (fullrawout_sig >> (self.sigWidth + 2)) & 1
        roundUp = guardBit and (roundBit or stickyBit or (not roundBit and not stickyBit and leastSigBitOfResult))
        if notNaN_isZeroOut or a_iszero or b_iszero:
            preRoundSig = fullrawout_sig
        else:
            preRoundSig = fullrawout_sig >> (self.sigWidth + 2)
        #print(f"preRoundSig: {preRoundSig}")
        #print(f"roundUp: {roundUp}")
        if roundUp:
            rawOut_sig = preRoundSig + 1
        else:
            rawOut_sig = preRoundSig
        #print(f"rawOut_sig: {rawOut_sig}")
        if (rawOut_sig >> self.sigWidth) & 1:
            rawOut_exp = fullrawout_exp + 1
        else:
            rawOut_exp = fullrawout_exp
        # if notNaN_isZeroOut or a_iszero or b_iszero:
        #     print("here")
        #     self.rawOut.exp = fullrawout_exp
        #     self.rawOut.sig = fullrawout_sig
        # else:
        self.rawOut.exp = rawOut_exp
        self.rawOut.sig = rawOut_sig & ((1 << self.sigWidth) - 1)
        #print(rawOut_exp)
        

def adder(input_1, input_2, expWidth, sigWidth):
    addRaw = AddRawFN(expWidth, sigWidth)


    a_exp, a_sig = float_to_bin(input_1, expWidth, sigWidth)
    b_exp, b_sig = float_to_bin(input_2, expWidth, sigWidth)
    '''
    
    if a_exp <0 or b_exp <0 or a_sig <0 or b_sig <0:
        print(f"input_1 {input_1} {a_exp} {a_sig}, input_2 {input_2} {b_exp} {b_sig}")
        raise ValueError("Invalid int exp_int  or sig_int")
    #print(f"Input exp: {a_exp}, sig: {a_sig}")
    '''
    if a_exp <0 :
        a_exp==0
    if b_exp <0 :
        b_exp==0


    # Example inputs
    addRaw.a.exp = a_exp
    addRaw.a.sig = a_sig
    addRaw.b.exp = b_exp
    addRaw.b.sig = b_sig

    addRaw.compute()
    '''
    
    if addRaw.rawOut.exp <0 or addRaw.rawOut.sig <0:
        print(f"input_1 {input_1}, input_2 {input_2}")
        raise ValueError("Invalid out exp_int  or out sig_int")
    '''
    output = bin_to_float(addRaw.rawOut.exp, addRaw.rawOut.sig, expWidth, sigWidth)
    #print(f"Output : {output}")
    #print(f"Output exp: {addRaw.rawOut.exp}, sig: {addRaw.rawOut.sig}")
    #error = abs(random_float_1+random_float_2-output)
    #print(f"Error: {error}")
    #if error > 8.267534372663476e-07:
        #print(f"Error: {error}")
        #print(f"random_float_1+random_float_2: {random_float_1+random_float_2}")
    
    return output
#adder(0.9, 0.9, 8, 23)  


# # muptiplier

# %%


class MulFullRawFN:
    def __init__(self, expWidth, sigWidth):
        self.expWidth = expWidth
        self.sigWidth = sigWidth
        self.a = RawFloat(expWidth, sigWidth)
        self.b = RawFloat(expWidth, sigWidth)
        self.rawOut = RawFloat(expWidth, (sigWidth + 1) * 2)

    def compute(self):
        a_iszero = (self.a.exp == 0) and (self.a.sig == 0)
        b_iszero = (self.b.exp == 0) and (self.b.sig == 0)
        notNaN_isZeroOut = a_iszero or b_iszero
        bias = (1 << (self.expWidth - 1)) - 1
        common_expOut = self.a.exp + self.b.exp - bias
        common_sigOut = ((1 << self.sigWidth) + self.a.sig) * ((1 << self.sigWidth) + self.b.sig)

        #print(f"common_expOut: {common_expOut}")
        # print(f"(common_sigOut >> ((self.sigWidth + 1) * 2 - 1)) & 1: {(common_sigOut >> ((self.sigWidth + 1) * 2 - 1)) & 1}")

        # mask = (1 << self.sigWidth) - 1
        if notNaN_isZeroOut:
            self.rawOut.exp = 0
            self.rawOut.sig = 0
        elif (common_sigOut >> ((self.sigWidth + 1) * 2 - 1)) & 1:
            self.rawOut.exp = common_expOut + 1
            self.rawOut.sig = circular_left_shift(common_sigOut, 1, (self.sigWidth + 1) * 2)
        else:
            self.rawOut.exp = common_expOut
            self.rawOut.sig = circular_left_shift(common_sigOut, 2, (self.sigWidth + 1) * 2)
        # print(f"self.rawOut.sig: {self.rawOut.sig}")
class MulRawFN:
    def __init__(self, expWidth, sigWidth):
        self.expWidth = expWidth
        self.sigWidth = sigWidth
        self.a = RawFloat(expWidth, sigWidth)
        self.b = RawFloat(expWidth, sigWidth)
        self.rawOut = RawFloat(expWidth, sigWidth)
        self.mulFullRaw = MulFullRawFN(expWidth, sigWidth)

    def compute(self):
        self.mulFullRaw.a = self.a
        self.mulFullRaw.b = self.b
        self.mulFullRaw.compute()
        
        sig = self.mulFullRaw.rawOut.sig
        exp = self.mulFullRaw.rawOut.exp

#######################
        guardBit = (sig >> (self.sigWidth + 1)) & 1  # G
        roundBit = (sig >> self.sigWidth) & 1  # R
        stickyBit = any([(sig >> i) & 1 for i in range(self.sigWidth)])  # S
        leastSigBitOfResult = (sig >> (self.sigWidth + 2)) & 1

        # Determine if we should round up
        roundUp = guardBit and (roundBit or stickyBit or (not roundBit and not stickyBit and leastSigBitOfResult))

        # Extract the significant bits before rounding
        preRoundSig = (sig >> (self.sigWidth + 2)) & ((1 << (self.sigWidth + 1)) - 1)

        # Apply rounding
        if roundUp:
            rawOut_sig = preRoundSig + 1
        else:
            rawOut_sig = preRoundSig

        # Check if the most significant bit of the result is set after rounding
        if (rawOut_sig >> self.sigWidth) & 1:
            rawOut_exp = exp + 1
        else:
            rawOut_exp = exp

        # # Truncate the result to the desired width
        # rawOut_sig_reg = rawOut_sig & ((1 << self.sigWidth) - 1)
        # rawOut_exp_reg = rawOut_exp  # Assuming expWidth is large enough to hold the result
#######################
        self.rawOut.exp = rawOut_exp
        self.rawOut.sig = rawOut_sig & ((1 << self.sigWidth) - 1)
        #print("rawOut_exp",rawOut_exp)
        #print(rawOut_sig)
def muptiplier(input_1, input_2, expWidth, sigWidth):
    mulRaw = MulRawFN(expWidth, sigWidth)
    a_exp, a_sig = float_to_bin(input_1, expWidth, sigWidth)
    b_exp, b_sig = float_to_bin(input_2, expWidth, sigWidth)
    '''
    if a_exp <0 or b_exp <0 or a_sig <0 or b_sig <0:
        print(f"input_1 {input_1} {a_exp} {a_sig}, input_2 {input_2} {b_exp} {b_sig}")
        raise ValueError("Invalid int exp_int  or sig_int")
    '''
    
    
    if a_exp <0 :
        a_exp==0
    if b_exp <0 :
        b_exp==0

    # Example inputs
    mulRaw.a.exp = a_exp
    mulRaw.a.sig = a_sig
    mulRaw.b.exp = b_exp
    mulRaw.b.sig = b_sig

    mulRaw.compute()
    output = bin_to_float(mulRaw.rawOut.exp, mulRaw.rawOut.sig, expWidth, sigWidth)
    '''
    
    if mulRaw.rawOut.exp <0 or mulRaw.rawOut.sig <0:
        print(f"input_1 {input_1}, input_2 {input_2}")
        raise ValueError("Invalid out exp_int  or out sig_int")
    '''
    return output
#muptiplier(1.125,2, 8, 6)    
#print(   float_to_bin(0.0698, 5, 20)    )
#print(muptiplier(0.0698,0.0698, 5, 20)  )
#print(  float_to_bin(0.00487204, 5, 20)    )
# # Approximate multiplier     

# %%


def error_constant_to_binary_fraction(decimal, bit_width):
    binary_fraction = ""
    for _ in range(bit_width):
        decimal *= 2
        int_part = int(decimal)
        binary_fraction += str(int_part)
        decimal -= int_part
    return binary_fraction
        
class Approx_multi_RawFN:
    def __init__(self, expWidth, sigWidth):
        self.expWidth = expWidth
        self.sigWidth = sigWidth
        self.a = RawFloat(expWidth, sigWidth)
        self.b = RawFloat(expWidth, sigWidth)
        self.rawOut = RawFloat(expWidth, sigWidth)
        




    def multiply(self):
    
        a_iszero = (self.a.exp == 0) and (self.a.sig == 0)
        b_iszero = (self.b.exp == 0) and (self.b.sig == 0)
        notNaN_isZeroOut = a_iszero or b_iszero

        bias = (1 << (self.expWidth - 1)) - 1

        rawOut_exp = self.a.exp - bias + self.b.exp
        rawOut_sig = self.a.sig + self.b.sig
        #print('self.a.sig:',self.a.sig)
        #print('self.b.sig:',self.b.sig)

        #print('rawOut_sig:',rawOut_sig)
        #print('self.sigWidth:',self.sigWidth)
        

        C = 0.08333
        binary_C = error_constant_to_binary_fraction(C, self.sigWidth)
        half_binary_C = error_constant_to_binary_fraction(0.5*C, self.sigWidth)
        error_constant=int(int(binary_C,2))
        half_error_constant=int(int(half_binary_C,2))
        #print('half_binary_C:',half_binary_C)
        #print('error_constant:',error_constant)
        #print('half_error_constant:',half_error_constant)
        if notNaN_isZeroOut:
            result_exp = 0
            result_sig = 0
        elif (rawOut_sig >> self.sigWidth) == 1:
            result_exp = rawOut_exp + 1
            result_sig = (rawOut_sig & ((1 << self.sigWidth) - 1))
        else:
            result_exp = rawOut_exp
            result_sig = (rawOut_sig & ((1 << self.sigWidth) - 1))
        #print('rawOut_sig;',rawOut_sig)  
        #print('1 << self.sigWidth) - 1;',(1 << self.sigWidth) - 1)
        #print('result_sig:',result_sig)

        self.rawOut.exp = result_exp
        self.rawOut.sig = result_sig
        
def app_muptiplier(input_1, input_2, expWidth, sigWidth):
    app_mulRaw = Approx_multi_RawFN(expWidth, sigWidth)
    a_exp, a_sig = float_to_bin(input_1, expWidth, sigWidth)
    b_exp, b_sig = float_to_bin(input_2, expWidth, sigWidth)
    '''
    if a_exp <0 or b_exp <0 or a_sig <0 or b_sig <0:
        print(f"input_1 {input_1} {a_exp} {a_sig}, input_2 {input_2} {b_exp} {b_sig}")
        raise ValueError("Invalid int exp_int  or sig_int")
    '''

    
    if a_exp <0 :
        a_exp==0
    if b_exp <0 :
        b_exp==0

    # Example inputs
    app_mulRaw.a.exp = a_exp
    app_mulRaw.a.sig = a_sig
    app_mulRaw.b.exp = b_exp
    app_mulRaw.b.sig = b_sig

    app_mulRaw.multiply()
    output = bin_to_float(app_mulRaw.rawOut.exp, app_mulRaw.rawOut.sig, expWidth, sigWidth)
    '''
    if app_mulRaw.rawOut.exp <0  or app_mulRaw.rawOut.sig <0:
        print(f"input_1 {input_1}, input_2 {input_2}")
        raise ValueError("Invalid out exp_int  or out sig_int")
    '''


    return output

#muptiplier(1.125,2, 8, 6)    
#print(   float_to_bin(0.0698, 5, 20)    )
#print(muptiplier(0.004,0.004, 3,23)  )
#print(  float_to_bin(0.00487204, 5, 20)    )
#print(app_muptiplier(0.04,0.04, 5,23) )        


# # MAP/MAR accuracy

# %%


def productnode_exact(input_1,input_1_info, input_2,input_2_info, expWidth, sigWidth):
    output=muptiplier(input_1, input_2, expWidth, sigWidth)
    output_info=str(input_1_info+input_2_info)
    return output, output_info

def productnode_distribution(input_1,input_1_info, input_2,input_2_info, expWidth, sigWidth):
    output=muptiplier(input_1, input_2, expWidth, sigWidth)
    exp_int_in1, sig_int_in1 = float_to_bin(input_1, expWidth, sigWidth)
    exp_int_in1 = exp_int_in1 - (2**(expWidth - 1) - 1) if exp_int_in1 != 0 else exp_int_in1
    sig_int_in1 = (sig_int_in1 / (1 << sigWidth))
    exp_int_in2, sig_int_in2 = float_to_bin(input_2, expWidth, sigWidth)
    exp_int_in2 = exp_int_in2 - (2**(expWidth - 1) - 1) if exp_int_in2 != 0 else exp_int_in2
    sig_int_in2 = (sig_int_in2 / (1 << sigWidth))
    distribute_list=[exp_int_in1,sig_int_in1,exp_int_in2,sig_int_in2 ]    
    output_info=(distribute_list)
    return output, output_info

def productnode_approximate(input_1,input_1_info, input_2,input_2_info, expWidth, sigWidth):
    output=app_muptiplier(input_1, input_2, expWidth, sigWidth)
    output_info=str(input_1_info+input_2_info)
    return output, output_info

def maxnode_exact(input_1,input_1_info, input_2,input_2_info, expWidth, sigWidth):
    output = max(input_1,input_2)
    output_info=str(input_1_info)if input_1>input_2 else  str(input_2_info)
    return output, output_info
    
def maxnode_distribution(input_1,input_1_info, input_2,input_2_info, expWidth, sigWidth):

    output = max(input_1,input_2)
    #output_info=[input_1_info,input_2_info]
    E=input_1_info[0]+input_1_info[2]-input_2_info[0]-input_2_info[2]
    acc_M=math.log2(1+input_1_info[1])+math.log2(1+input_1_info[3])-math.log2(1+input_2_info[1])-math.log2(1+input_2_info[3])
    app_M=input_1_info[1]+input_1_info[3]-input_2_info[1]-input_2_info[3]
    output_info=[E,acc_M,app_M,(E+acc_M)*(E+app_M)]
    #[[-1, 0.9669845928099781, 0, 0.0], [-6, 0.056493030080704276, 0, 0.0]]
    print(output_info)
    return output, output_info
    
    
#EL1+EL2+math.log2(1+ML1)+math.log2(1+ML2)<=ER1+ER2+math.log2(1+MR1)+math.log2(1+MR2):
#EL1+EL2+ML1+ML2>ER1+ER2+MR1+MR2:    
def sumnode_for_sampling(input_1,input_1_info, input_2,input_2_info, expWidth, sigWidth):
    output = adder(input_1, input_2, expWidth, sigWidth)
    random_number = random.random()
    if input_1 >= input_2:
        if random_number >= input_2:
            output_info = str(input_1_info)
        else:
            output_info = str(input_2_info)
    else:
        if random_number >= input_1:
            output_info = str(input_2_info)
        else:
            output_info = str(input_1_info)
    return output, output_info
#sumnode_for_sampling(0.6,'input1', 0.4,'input2',8,4)

def sumnode(input_1,input_1_info, input_2,input_2_info, expWidth, sigWidth):
    output = adder(input_1, input_2, expWidth, sigWidth)
    output_info=str(input_1_info)if input_1>input_2 else  str(input_2_info)
    return output, output_info
def logerror(input):
    if input == 0:
        return 0
    output = math.log2(1+(np.frexp(input)[0]- 0.5) * 2)-(np.frexp(input)[0]- 0.5) * 2
    return output


# %%





# %%

import sys
def distribution_spn(model, inputfile, p, s, e, m):
    global productnodevalue
    global maxnodevalue
    global expWidth
    global sigWidth
    productnodevalue = p
    maxnodevalue = s
    expWidth = e
    sigWidth = m
    #percentage_to_choose=0.4
    # Initialize the dictionary to store weights
    #weight_dict = {}
    with open('./Data/weights_'+str(model)+'_new.txt', "r") as f:
        for line in f:
            exec(line, globals())

    # Create 16 * 2 variables from 0 to 15
    if model == 'nltcs':
        variables = ['v{}{}'.format(i, suffix) for i in range(16) for suffix in ['a', 'b']]
    if model == 'jester':
        variables = ['v{}{}'.format(i, suffix) for i in range(100) for suffix in ['a', 'b']]       
    if model == 'dna':
        variables = ['v{}{}'.format(i, suffix) for i in range(180) for suffix in ['a', 'b']]      
    if model == 'book':
        variables = ['v{}{}'.format(i, suffix) for i in range(500) for suffix in ['a', 'b']]     
    # Initialize info variables in a dictionary
    eval_env = {}
    for var in variables:
        eval_env["{}_info".format(var)] = str(var)
        
    original_op_value = [] 
    original_op_info_value = [] 
    # Read the variable from the input file and update variables in eval_env   
    with open('output_log_'+str(model)+'.txt', 'w') as output_file:
    # Read and process each input line
        with open(inputfile, 'r') as file:
            for input_line in file:
                input_values = input_line.strip().split(',')
                #print(input_values)
                for var, value in zip(variables, input_values):
                    eval_env[var] = float(value)
                # Capture the output for each input line in a sublist
                captured_output = []
                # Redirect stdout to capture print outputs temporarily
                original_stdout = sys.stdout
                sys.stdout = output_file  # Redirect to file, consider using StringIO to capture instead
    
                # Read and execute operations for each input line
                with open('./Data/operations_' + str(model) + '_new.txt', 'r') as ops_file:
                    for line in ops_file:
                        exec(line, globals(), eval_env)
    
                # Restore stdout
                sys.stdout = original_stdout
    
                # Write the captured output as a list (sublist for each input line)
                output_file.write(str(captured_output) + '\n')  # Each sublist is written as a new line


#distribution_spn('nltcs', './Data/nltcs'+'_input_aftersampling.txt',productnode_distribution, maxnode_distribution, 11, 52) 


#EL1+EL2+math.log2(1+ML1)+math.log2(1+ML2)<=ER1+ER2+math.log2(1+MR1)+math.log2(1+MR2):
#EL1+EL2+ML1+ML2>ER1+ER2+MR1+MR2:


# %%


def compute_spn(model, inputfile, p, s, e, m):
    global productnodevalue
    global maxnodevalue
    global expWidth
    global sigWidth
    productnodevalue = p
    maxnodevalue = s
    expWidth = e
    sigWidth = m
    #percentage_to_choose=0.4
    # Initialize the dictionary to store weights
    #weight_dict = {}
    with open('./Data/weights_'+str(model)+'_new.txt', "r") as f:
        for line in f:
            exec(line, globals())

    # Create 16 * 2 variables from 0 to 15
    if model == 'nltcs':
        variables = ['v{}{}'.format(i, suffix) for i in range(16) for suffix in ['a', 'b']]
    if model == 'jester':
        variables = ['v{}{}'.format(i, suffix) for i in range(100) for suffix in ['a', 'b']]       
    if model == 'dna':
        variables = ['v{}{}'.format(i, suffix) for i in range(180) for suffix in ['a', 'b']]      
    if model == 'book':
        variables = ['v{}{}'.format(i, suffix) for i in range(500) for suffix in ['a', 'b']]     
    # Initialize info variables in a dictionary
    eval_env = {}
    for var in variables:
        eval_env["{}_info".format(var)] = str(var)
        
    original_op_value = [] 
    original_op_info_value = [] 
    # Read the variable from the input file and update variables in eval_env   
    with open(inputfile, 'r') as file:
        for input_line in file:
            input_values = input_line.strip().split(',')
            #print(input_values)
            for var, value in zip(variables, input_values):
                eval_env[var] = float(value)
                #print(eval_env)
            # Execute operations line by line
            with open('./Data/operations_'+str(model)+'_new.txt', 'r') as file:
                for line in file:
                    exec(line, globals(), eval_env)
                    last_line = line

        # Parse variable names from the last line
            if last_line:
                # Extract first and second variable names (before and after the comma)
                first_var, second_var = last_line.split("=")[0].strip().split(",")
                first_var = first_var.strip()  # Remove any extra spaces
                second_var = second_var.strip()  # Remove any extra spaces

            original_op_value.append(eval_env.get(first_var))
            original_op_info_value.append(eval_env.get(second_var))

    return original_op_value, original_op_info_value


#original_op_value, original_op_info_value=compute_spn('nltcs', './Data/nltcs'+'_all1_input.txt',productnode_approximate, sumnode, 8, 23) 




#print(original_op_value,original_op_info_value)


# %%


# Function to convert 'a' to '1,0' and 'b' to '0,1'
def convert_value(value):
    if value == 'a':
        return '1,0'
    elif value == 'b':
        return '0,1'
    else:
        return '1,1'  # Handle unexpected cases
def sampling_spn(model, inputfile):
    original_op_value, original_op_info_value = compute_spn(model, inputfile, productnode_exact, sumnode_for_sampling, 11, 52)
    #print(original_op_info_value)

    # Create a new file to write the output
    with open('./Data/'+str(model)+'_input_aftersampling.txt', 'w') as f:
        # Loop through each line in original_op_info_value
        for line in original_op_info_value:
            elements = line.strip().split()
            converted_elements = {}
            
            # Initializing binary information for each variable (both 'a' and 'b') to 0
            for element in elements:
                var_name = element[:-1]  # Extract the variable name, e.g., 'v0' from 'v0a'
                converted_elements[var_name + 'a'] = 0
                converted_elements[var_name + 'b'] = 0

            # Now set the binary information based on presence of each variable in the line
            for element in elements:
                converted_elements[element] = 1
            
            # Create the output line
            output_line = []
            for key in sorted(converted_elements.keys()):
                output_line.append(str(converted_elements[key]))
            
            # Writing the line into the file
            f.write(','.join(output_line) + ',\n')

    return

#sampling_spn('nltcs', './Data/nltcs'+'_all1_input.txt')
#sampling_spn('jester', './Data/jester'+'_all1_input.txt')
#sampling_spn('dna', './Data/dna'+'_all1_input.txt')
#sampling_spn('book', './Data/book'+'_all1_input.txt')


# %%





# %%
def get_normalization_constant(model, e, m, numbersystem, inference):
    # Construct the key and file path
    key = f"{model}_{e}_{m}_{numbersystem}_{inference}"
    file_path = f"./results/results_accuracy_{key}.txt"
    
    # Open and read the file
    with open(file_path, 'r') as f:
        data = f.read()
    
    # Parse the JSON content
    json_data = json.loads(data)
    
    # Extract and return the normalization_constant
    return json_data[key]['normalization_constant']



def accuracy_spn(model, inputfile, e, m, numbersystem, inference):
    numerical_loss_before = 'none'
    numerical_loss_after = 'none'
    string_accuracy = 'none'
    normalization_constant='none'
    if numbersystem == 'float' and inference == 'MAR':
        original_op_value, original_op_info_value = compute_spn(model,inputfile, productnode_exact, sumnode, 11, 52)  
        op_value, op_info_value = compute_spn(model,inputfile,  productnode_exact, sumnode, e, m)      

        
        # Compute the sum of squares for original_op_value and op_value
        original_op_value = np.array(original_op_value,dtype=np.float128)
        #print(original_op_value)
        op_value = np.array(op_value,dtype=np.float128)
        #print(op_value)
        
        mask = (original_op_value != 0) & (op_value != 0)

        filtered_original = original_op_value[mask]
        filtered_op = op_value[mask]
        #print("Types:", type(original_op_value), type(op_value), type(mask))
        #print("Shapes:", original_op_value.shape, op_value.shape, mask.shape)

        if len(filtered_original) > 0:
            numerical_loss_before = np.mean(np.log(filtered_original) - np.log(filtered_op))
        else:
            numerical_loss_before= 'none'  # or some other value 

            
        if len(filtered_original) > 0:
            numerical_loss_after = np.mean(np.log(filtered_original) - np.log(filtered_op))
        else:
            numerical_loss_after= 'none'  # or some other value        
        #numerical_loss = 100*sum([abs(o - p)/o for o, p in zip(original_op_value, op_value)])/len(original_op_value)
  
        #zero_array = np.zeros_like(original_op_value)
        #sum_of_squares_original = sum([x**2 for x in original_op_value])
        #sum_of_squares_diff = sum([(o - p)**2 for o, p in zip(original_op_value, op_value)])
        #numerical_loss = 100*abs(sum_of_squares_diff ) / sum_of_squares_original
        #print(sum_of_squares_original)
        #print(sum_of_squares_diff)
        
        string_accuracy='none'
        normalization_constant='none'
        #print(sum_of_squares_original)
        #print(sum_of_squares_diff)
 

    elif numbersystem == 'app' and inference == 'MAR':
        original_op_value, original_op_info_value = compute_spn(model, inputfile,productnode_exact, sumnode, 11, 52)  
        op_value, op_info_value = compute_spn(model, inputfile, productnode_approximate, sumnode,e, m) 
        # Calculate normalization constant, avoiding division by zero
        #print('original_op_value:',original_op_value)
        #print('op_value:',op_value)
        from decimal import Decimal, getcontext

        ratios = [p / o if o != 0 else 1 for p, o in zip(op_value, original_op_value)]
        error=[abs(p - o )if o != 0 else 1 for p, o in zip(op_value, original_op_value)]
        #print('ratios:',ratios)
        #normalization_constant = 553


        '''
        
        # use this when run in sampling set
        normalization_constant = sum(ratios) / len(ratios) if sum(ratios) > 0 else 1  # Using 1 as a fallback value
        error_term= sum(error) / len(error) if sum(error) > 0 else 0 
        #print('error_term:',error_term)



        '''
        #  use this when run in test set
        key = f"{model}_{e}_{m}_{numbersystem}_{inference}"
        file_path = f"./results/results_accuracy_{key}.txt"
        # Open and read the file
        with open(file_path, 'r') as f:
            data = f.read()
        # Parse the JSON content
        json_data = json.loads(data)
        # Extract the normalization_constant
        normalization_constant = json_data[key]['normalization_constant']
        
        






        normalized_op_value = [value / normalization_constant for value in op_value]
        non_normalized_op_value = [value  for value in op_value]
        #normalized_op_value = [value / 1.0 for value in op_value]
        #normalized_op_value = [value - error_term for value in op_value]
        #print(original_op_value, normalized_op_value)
        

         
        original_op_value = np.array(original_op_value,dtype=np.float128)
        
        normalized_op_value = np.array(normalized_op_value,dtype=np.float128)
        non_normalized_op_value = np.array(non_normalized_op_value,dtype=np.float128)
        #print('normalized_op_value:',normalized_op_value)
        mask = (original_op_value != 0) & (normalized_op_value != 0)
        #mask = (original_op_value > 0) & (normalized_op_value > 0)
        filtered_original = original_op_value[mask]
        filtered_op_after = normalized_op_value[mask]
        filtered_op_before = non_normalized_op_value[mask]
        #abs for test set
        if len(filtered_original) > 0:
            numerical_loss_after = np.mean(abs(np.log(filtered_original) - np.log(filtered_op_after)))
        else:
            numerical_loss_after = 'none'  # or some other value 

        if len(filtered_original) > 0:
            numerical_loss_before = np.mean(abs(np.log(filtered_original) - np.log(filtered_op_before)))
        else:
            numerical_loss_before = 'none'  # or some other value         

        #numerical_loss = 100*sum([abs(o - p)/o for o, p in zip(original_op_value,normalized_op_value)])/len(original_op_value)
        
        
        #zero_array = np.zeros_like(original_op_value)
        #sum_of_squares_original = sum([x**2 for x in original_op_value])
        #sum_of_squares_diff = sum([(o - p)**2 for o, p in zip(original_op_value, normalized_op_value)])
        #numerical_loss = 100*abs(sum_of_squares_diff ) / sum_of_squares_original
        
        #print(sum_of_squares_original)
        #print(sum_of_squares_diff)        
  
        string_accuracy='none'
        
    elif numbersystem == 'float' and inference == 'MAP':
        original_op_value, original_op_info_value = compute_spn(model,inputfile, productnode_exact, maxnode_exact, 11, 52)    
        op_value, op_info_value = compute_spn(model, inputfile, productnode_exact, maxnode_exact,e, m) 
        # Count the number of exact matches for string values
        # Initialize counts for matches and total elements
        total_count = 0
        match_count = 0

        # Iterate over each string in the original and new lists
        for original, new in zip(original_op_info_value, op_info_value):
            # Split the string into its constituent parts
            original_parts = original.strip().split()
            new_parts = new.strip().split()

            # Increment the total count and match count based on comparisons
            for o, n in zip(original_parts, new_parts):
                total_count += 1
                if o == n:
                    match_count += 1

        # Calculate the ratio of exact matches to the total number of elements
        string_accuracy = match_count / total_count if total_count > 0 else 0
        numerical_loss_before='none' 
        numerical_loss_after='none' 
        normalization_constant='none'      
    elif numbersystem == 'app' and inference == 'MAP':
        original_op_value, original_op_info_value = compute_spn(model, inputfile,productnode_exact, maxnode_exact, 11, 52)    
        op_value, op_info_value = compute_spn(model,inputfile,  productnode_approximate, maxnode_exact,e, m) 
        # Initialize counts for matches and total elements
        total_count = 0
        match_count = 0

        # Iterate over each string in the original and new lists
        for original, new in zip(original_op_info_value, op_info_value):
            # Split the string into its constituent parts
            original_parts = original.strip().split()
            new_parts = new.strip().split()

            # Increment the total count and match count based on comparisons
            for o, n in zip(original_parts, new_parts):
                total_count += 1
                if o == n:
                    match_count += 1

        # Calculate the ratio of exact matches to the total number of elements
        string_accuracy = match_count / total_count if total_count > 0 else 0
        numerical_loss_before='none' 
        numerical_loss_after='none' 
        normalization_constant='none'
    
    


    return numerical_loss_before, numerical_loss_after, string_accuracy,normalization_constant


#print(original_op_info_value)
#print(op_value)
#print(op_info_value)
#print(string_accuracy)
#print('numerical_loss_nltcs',numerical_loss_nltcs)

## Initialize dictionary to store results
#print('numerical_loss for replace all in log error:',numerical_loss)


# %%





# %%


def modify_circuit_replacement_spn(model,percentage_to_choose,selection_method, det_method):
    global productnodevalue
    global productnodevalue_new
    global maxnodevalue
    global expWidth
    global sigWidth
    variable_order = []
    expWidth=11
    sigWidth=52
    maxnodevalue=sumnode
    productnodevalue=productnode_exact
    productnodevalue_new=productnode_approximate
    variables = {}
    new_variables = {}

    if model == 'nltcs':
        variable_order = ['v{}{}'.format(i, suffix) for i in range(16) for suffix in ['a', 'b']]
    if model == 'jester':
        variable_order = ['v{}{}'.format(i, suffix) for i in range(100) for suffix in ['a', 'b']]       
    if model == 'dna':
        variable_order = ['v{}{}'.format(i, suffix) for i in range(180) for suffix in ['a', 'b']]      
    if model == 'book':
        variable_order = ['v{}{}'.format(i, suffix) for i in range(500) for suffix in ['a', 'b']]    

    for var in variable_order:
        variables["{}_info".format(var)] = str(var)  
        new_variables["{}_info".format(var)] = str(var)
    with open('./Data/weights_'+str(model)+'_new.txt', "r") as f:
        for line in f:
            exec(line, globals()) 




    def calculate_average_deltas(delta_sums, line_count):
        return {index: total_delta / line_count for index, total_delta in delta_sums.items()}

    delta_sums = {}
    original_op_value_list = [] 
    line_count = 0  # Counter to track the number of lines processed.
    #with open('example_all1_input.txt', 'r') as file: 
    with open('./Data/'+str(model)+'_input_aftersampling.txt', 'r') as file:
        for input_line in file:
            line_count += 1  # Increment the line counter.
            values = input_line.strip().split(',')
            for var_name, value in zip(variable_order, values):
                if det_method == 'nondet':
                    variables[var_name] = float(value)
                    new_variables[var_name] = float(value)
                if det_method == 'det':
                    variables[var_name] = float(1)   
                    new_variables[var_name] = float(value)
            #print(variables)
            #print(new_variables)
            # Evaluate original circuit
            new_lines = []
            pattern = r"(.+?),(.+?)=productnodevalue\((.+?),.+?,(.+?),.+?,.+,.+\)"
            with open('./Data/operations_'+str(model)+'_new.txt', 'r') as file:

                for line in file:
                    exec(line, globals(), new_variables)

                    new_lines.append(line)
                    if 'weight' in line:
                        match = re.search(pattern, line)
                        if match:
                            weight_param = match.group(4)  # the parameter that contains 'weight'
                            output_param = match.group(1)  # the first output parameter                
                            new_lines.append('delta=logerror({})*({})'.format(weight_param, output_param))


                last_line = line
                if last_line:
                # Extract first and second variable names (before and after the comma)
                    first_var, second_var = last_line.split("=")[0].strip().split(",")
                    first_var = first_var.strip()  # Remove any extra spaces
                    original_op_value = new_variables.get(first_var)
            #print(original_op_value)
            original_op_value_list.append(original_op_value)
            #print(new_variables)
    #get the delat according to all input data points 
            deltas = []
            productnode_indexes = []



            for index, line in enumerate(new_lines):
                if line.startswith('delta'):
                    exec(line, globals(), variables)
                    deltas.append((variables['delta'], productnode_indexes[-1]))
                else:
                    exec(line, globals(), variables)
                    if 'productnodevalue' in line:
                        productnode_indexes.append(index)

            for delta, index in deltas:
                if index not in delta_sums:
                    delta_sums[index] = 0.0
                delta_sums[index] += delta                

    #till here we finished the delta calculation and nre lines generation
    # Calculate average deltas 
    average_deltas = calculate_average_deltas(delta_sums, line_count)
    #other work that needs the average_deltas
    #print('len(average_deltas)',len(average_deltas))
    sorted_average_deltas = sorted(average_deltas.items(), key=lambda x: x[1])
    #print('len(sorted_average_deltas)',len(sorted_average_deltas))
    #print('len(productnode_indexes)',len(productnode_indexes))
    select_index = int(len(sorted_average_deltas) * float(percentage_to_choose))
    #print('len(sorted_average_deltas)',len(sorted_average_deltas))
    #print('percentage_to_choose',percentage_to_choose)
    #select_index_random = int(len(productnode_indexes) * percentage_to_choose)
    #select_index_random = int((select_index ))
    #print('(len(select_index))',(len(select_index)))
    indexes_to_modify = []

    if selection_method == 'small':
        indexes_to_modify = [index for index, _ in sorted_average_deltas[:select_index]]
    elif selection_method == 'random':
        #the previous version that only random sample from weights
        #indexes_to_modify = random.sample([index for index, _ in sorted_average_deltas], select_index)
        #indexes_to_modify = random.sample([index for index in productnode_indexes], select_index)
        indexes_to_modify = random.sample(productnode_indexes, select_index)
    #print(indexes_to_modify)
    for index in indexes_to_modify:
        line = new_lines[index]
        modified_line = line.replace('productnodevalue', 'productnodevalue_new')
        new_lines[index] = modified_line
    new_circuit = "\n".join(new_lines)
    # re evaluate according to the new circuit
    modified_op_value_list= [] 
    with open('./Data/'+str(model)+'_input_aftersampling.txt', 'r') as file:
        for input_line in file:
            values = input_line.strip().split(',')
            for var_name, value in zip(variable_order, values):
                new_variables[var_name] = float(value)
            # Evaluate modified circuit
            for new_line in new_circuit.split('\n'):
                #print(line)
                exec(new_line, globals(), new_variables)          
            modified_op_value = new_variables.get(first_var)                    
            modified_op_value_list.append(modified_op_value)
    sum_ratio = 0.0
    valid_count = 0
    # Calculate normalization constant
    for mod, orig in zip(modified_op_value_list, original_op_value_list):
        if orig != 0:
            sum_ratio += mod / orig
            valid_count += 1
    normalization_constant = sum_ratio / valid_count

    #print('ratios:',ratios)
    #print("normalization_constant:",normalization_constant)
    normalized_op_value_list = [value / normalization_constant for value in modified_op_value_list]
    non_normalized_op_value_list = [value  for value in modified_op_value_list]   
    #print("normalized_op_value_list:",normalized_op_value_list)
    original_op_value_list = np.array(original_op_value_list,dtype=np.float128)
    normalized_op_value_list = np.array(normalized_op_value_list,dtype=np.float128)
    non_normalized_op_value_list = np.array(non_normalized_op_value_list,dtype=np.float128)

    mask = (original_op_value_list != 0) & (normalized_op_value_list != 0)

    filtered_original = original_op_value_list[mask]
    filtered_op_after = normalized_op_value_list[mask]
    filtered_op_before = non_normalized_op_value_list[mask]

    if len(filtered_original) > 0:
        numerical_loss_after = np.mean(np.log(filtered_original) - np.log(filtered_op_after))
    else:
        numerical_loss_after = 'none'  # or some other value 

    if len(filtered_original) > 0:
        numerical_loss_before = np.mean(np.log(filtered_original) - np.log(filtered_op_before))
    else:
        numerical_loss_before = 'none'  # or some other value  

    actual_percentage=len(sorted_average_deltas)* float(percentage_to_choose)/len(productnode_indexes )
    return numerical_loss_before, numerical_loss_after, actual_percentage,normalization_constant
   


# %%





# %%

#numerical_loss_before, numerical_loss_after, string_accuracy,normalization_constant= accuracy_spn('nltcs', './Data/nltcs'+'_input_aftersampling.txt', 8, 12, 'app', 'MAR')
#numerical_loss_before, numerical_loss_after, actual_percentage,normalization_constant=modify_circuit_replacement_spn('nltcs',0.2,'small', 'nondet')




def main(dataset, e, m, data_type, metric):
    results_dict = {}
    #use it when run in smaple set
    #inputfile = str(dataset) + '_input_aftersampling.txt'
    # use it when run in test set
    inputfile = './Data/'+str(dataset) + '_test.txt'    
    numerical_loss_before, numerical_loss_after, string_accuracy,normalization_constant = accuracy_spn(dataset, inputfile, e, m, data_type, metric)
    #print(numerical_loss_before, numerical_loss_after, string_accuracy,normalization_constant)   
    key = f"{dataset}_{e}_{m}_{data_type}_{metric}"
    if isinstance(numerical_loss_before, np.float128):
        numerical_loss_before = float(numerical_loss_before)
    if isinstance(numerical_loss_after, np.float128):
        numerical_loss_after = float(numerical_loss_after)        
    results_dict[key] = {
        'numerical_loss_before': numerical_loss_before,
        'numerical_loss_after': numerical_loss_after,
        'string_accuracy': string_accuracy,
        'normalization_constant': normalization_constant 
    }

        # Specify the file path
    file_path = './test_results_mar/results_accuracy_' + key + '.txt'

    # Open the file in write mode and save the dictionary as JSON
    with open(file_path, 'w') as outfile:
        json.dump(results_dict, outfile, indent=4)









if __name__ == '__main__':


    # Parse command line arguments
   
    
    dataset = sys.argv[1]
    e = int(sys.argv[2])
    m = int(sys.argv[3])
    data_type = sys.argv[4]
    metric = sys.argv[5]
    main(dataset, e, m, data_type, metric)
   
    #numerical_loss_before, numerical_loss_after, string_accuracy,normalization_constant= accuracy_spn('jester', 'jester'+'_input_aftersampling.txt', 8, 52, 'app', 'MAR')
    #numerical_loss_before, numerical_loss_after, actual_percentage,normalization_constant=modify_circuit_replacement_spn('nltcs',0.2,'small', 'nondet')
    #print(numerical_loss)
    #numerical_loss 0.003 for nltcs under normalization
    #numerical_loss -1.9 for nltcs under mantissa correction
    #numerical_loss -19 for dna under mantissa correction
    #-1.2438209905372086368 for nltcs under mantissa correction and error corrrection
    #0.9849693195484391302 under error corrrection
    #print(numerical_loss_before, numerical_loss_after, string_accuracy,normalization_constant)   

 



