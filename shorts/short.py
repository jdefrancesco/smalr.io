#!/usr/bin/env python
##############################################################################################
# Author: in70x, Madhax
# Date:   8/21/2013
# 
# Description: shorts module that handles conversion
# 
#
#
#
# Last Updated: 9/22/2013
# Copyright (c) smalr.io
################################################################################################

import types

# Base we will use for conversions Ex: 125_base10 = cb_base62
BASE = 62

# Offset of characters into ASCII table
DIGIT_OFFSET = 48 # 48 is ASCII 0
UPPERCASE_OFFSET = 55 # 65 - 10
LOWERCASE_OFFSET = 61 # 97 - 36 (gives us our last characters - ends at 61st offset)

# LAYOUT OF CHARACTER TABLE
# [0-9A-Za-z] 

# Define exceptions
class ConvException(Exception): pass
class OutOfRangeError(ConvException): pass
class NonIntegerError(ConvException): pass
class InvalidBase62Value(ConvException): pass


# The following functions convert from base62 to Integer and vica-versa
def base62_map_integer(char_value):
    """
    Take an character from base62 system and turn back into
    integer equivalent...
    Ex: a --> 36 (a maps to 36)
    """

    if char_value.isdigit():
        return ord(char_value) - DIGIT_OFFSET 
    elif 'A' <= char_value <= 'Z':
        return ord(char_value) - UPPERCASE_OFFSET
    elif 'a' <= char_value <= 'z':
        return ord(char_value) - LOWERCASE_OFFSET
    else:
        raise ValueError("%s is not a valid character!" % repr(char_value))

    # -- EOFunc

def integer_map_base62(int_value):
    """
    Take an integer and produce its base62 character equivalent
    Ex: 36 --> a  (that is 36 maps to character a)
    """

    if int_value< 10:
        return chr(int_value + DIGIT_OFFSET)
    elif 10 <= int_value <= 35:
        return chr(int_value + UPPERCASE_OFFSET)
    elif 36 <= int_value < 62:
        return chr(int_value + LOWERCASE_OFFSET)
    else:
        return ValueError("%s is not a valid integer [0-61]!", repr(int_value))

    # -- EOFunc

def base10_to_base62(number):
    """
    Take a number and convert it to a list of base62 values
    Ex: let f() be current function. f('125') = [2, 1]
    """

    # We shouldn't get here (sanity check)
    if not isinstance(number, int) and not isinstance(number, long):
        raise NonIntegerError("Supplied parameter was not an integer %s " % repr(number))
        number = int(number) # Give us an integer

    # If we have a negative number, raise exception and covert to positive integer
    if number < 0:
        raise OutOfRangeError("Negative value supplied.. %s" % repr(number))
        number = abs(number)

    digits = []

    while number > 0:
        remainder = number % BASE
        digits.append(remainder)
        number /= BASE 

    digits.reverse() # We pushed values onto list backwards

    return digits

    # -- EOFunc

def base62_to_base10(b62_value):
    """
    Convert value that is currently base-62 back to base-10 
    equivalent.
    """

    if type(b62_value) is not types.StringType:
        raise InvalidBase62Value("Parameter should be string %s " % (repr(b62_value)))

    # Convert digits to a list and then reverse them to calculate integer equiv.
    digit_list = list(b62_value)
    digit_list.reverse()
   
    # Convert base-62 to base-10: (xN*62^N)+(x1*62^1)+(x0*62^0)  
    sum = 0
    pow = 0
    for digit in digit_list:
        digit = base62_map_integer(digit)
        sum += digit * (BASE**pow)
        pow += 1

    return sum

def value_encode62(int_value):
    """
    Takes an integer value for input and returns the base62
    equivalent
    This is the interface that will be called when shortnening a link
    """
    # Be sure we are dealing with an integer
    int_value = int(int_value)

    # If negative convert to positive
    if int_value < 0:
        int_value = abs(int_value)

    # value_list will contain a list of digits (base 62) that constitute the value
    value_list = base10_to_base62(int_value)

    # Create a string that equivalent to our input integer
    encoded_string = ""
    for value in value_list:
        encoded_string += integer_map_base62(value)

    # return our 'short' url postfix
    return encoded_string

    # -- EOFunc


# LinkShortner Class - Creats and manipulates shortlinks..
class LinkShortner(object):
    def __init__(self):
        pass


def main():
    pass

    # -- EOFunc

if __name__ == '__main__': pass 
