#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 08:43:41 2022

@author: joaquinsalas
"""

from math import *

#First set up a input and convert input to an int number 

print('Please enter the number of digits of precision for e:')
exp = int(input(''))
#Created an f string that makes the precision change along with the number being inputed.
print(f'The value of e to {exp} digits is: {e:.{exp}f}')
