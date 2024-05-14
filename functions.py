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
    #print("exp is", exp_bin)
    #print("sig is", significand)
    exp_int = int(exp_bin, 2)
    sig_int = int(significand, 2)
    
    return exp_int, sig_int


def bin_to_float(exp, sig, exp_width, sig_width):
    bias = (1 << (exp_width - 1)) - 1
    exponent_result = exp - bias
    # print(f"exponent_result: {exponent_result}")
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

    #print(f"Input exp: {a_exp}, sig: {a_sig}")


    # Example inputs
    addRaw.a.exp = a_exp
    addRaw.a.sig = a_sig
    addRaw.b.exp = b_exp
    addRaw.b.sig = b_sig

    addRaw.compute()
    output = bin_to_float(addRaw.rawOut.exp, addRaw.rawOut.sig, expWidth, sigWidth)
    #print(f"Output : {output}")
    #print(f"Output exp: {addRaw.rawOut.exp}, sig: {addRaw.rawOut.sig}")
    #error = abs(random_float_1+random_float_2-output)
    #print(f"Error: {error}")
    #if error > 8.267534372663476e-07:
        #print(f"Error: {error}")
        #print(f"random_float_1+random_float_2: {random_float_1+random_float_2}")
    return output
print("adder(1.5,2, 5,23)",adder(1.5,2, 5,23))  


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

        # print(f"common_sigOut: {common_sigOut}")
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
        #print(rawOut_exp)
        #print(rawOut_sig)
def muptiplier(input_1, input_2, expWidth, sigWidth):
    mulRaw = MulRawFN(expWidth, sigWidth)
    a_exp, a_sig = float_to_bin(input_1, expWidth, sigWidth)
    b_exp, b_sig = float_to_bin(input_2, expWidth, sigWidth)
    print('a_exp:',a_exp)
    # Example inputs
    mulRaw.a.exp = a_exp
    mulRaw.a.sig = a_sig
    mulRaw.b.exp = b_exp
    mulRaw.b.sig = b_sig

    mulRaw.compute()
    output = bin_to_float(mulRaw.rawOut.exp, mulRaw.rawOut.sig, expWidth, sigWidth)

    return output
print("muptiplier(1.5,2, 5,23)",muptiplier(5.66766875*10**(-34),1.233444445*10**(-34), 11,23))  


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
    #print('a_exp:',a_exp)
    #print('a_sig:',a_sig)
    # Example inputs
    app_mulRaw.a.exp = a_exp
    app_mulRaw.a.sig = a_sig
    app_mulRaw.b.exp = b_exp
    app_mulRaw.b.sig = b_sig

    app_mulRaw.multiply()
    output = bin_to_float(app_mulRaw.rawOut.exp, app_mulRaw.rawOut.sig, expWidth, sigWidth)
    return output
print("app_muptiplier(1.5,2,5,23)",app_muptiplier(1.5,2, 5,23) )   