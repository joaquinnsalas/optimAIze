"""
Created on Tue Sep 20 13:14:22 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Yuriy Astapov
#               Areen Bhayani
#               Joaquin Salas
#               Aaditya Srinivasan
# Section:      576
# Assignment:   LAB Topic 4: Boolean Expressions
# Date:         20 September 2022
from math import *
############ Part A ############
a = input('Enter True or False for a: ')
b = input('Enter True or False for b: ')
c = input('Enter True or False for c: ')

if a == "T" or a == "t" or a == "True":
    a = True
elif a == "F" or a == "f" or a == "False":
    a = False
#b
if b == "T" or b == "t" or b == "True":
    b = True
elif b == "F" or b == "f" or b == "False":
    b = False
#c
if c == "T" or c == "t" or c == "True":
    c = True
elif c == "F" or c == "f" or c == "False":
    c = False

############ Part B ############
test1 = a and b and c
print(f"a and b and c: {test1}")
test2 = a or b or c
print(f"a or b or c: {test2}")
############ Part C ############
xor = not((a == b) and (b == c) and (a == c))
odd = not((int(a)+int(b)+int(c))%2 == 0)
print('XOR:', xor)
print('Odd number:',odd)

