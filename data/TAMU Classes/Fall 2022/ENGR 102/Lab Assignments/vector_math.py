#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 09:37:07 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Joaquin Salas
# Section:      576
# Assignment:   LAB Topic 7: vector_math.py
# Date:         18 October 2022

from math import *
# Take the users input for two vectors

# split up the inputs into a list by adding the following command to the end of the input statement
vector_a = input('Enter the elements for vector A: ').split()
cont_a = 0
sq_a = 0
vector_b = input('Enter the elements for vector B: ').split()
cont_b = 0
sq_b = 0
# make a for loop and set variables to 0 so it can loop thru list 
for i in vector_a:
    number = float(vector_a[cont_a])
    sq_a += (number ** 2)
    cont_a += 1
    
mag_a = sqrt(sq_a)
print(f'The magnitude of vector A is {mag_a:.5f}')

for i in vector_b:
    number = float(vector_b[cont_b])
    sq_b += (number ** 2)
    cont_b += 1
    
mag_b = sqrt(sq_b)
print(f'The magnitude of vector B is {mag_b:.5f}')

#Vector addition by making a new for loop and settting functions to 0 above
cont_a = 0
cont_b = 0
plus = []
for i in vector_b:
    A = float(vector_a[cont_a])
    B = float(vector_b[cont_b])
    add = A + B
    plus.append(add)
    cont_a += 1
    cont_b += 1
print(f'A + B is {plus}')
    
# For vector subtraction create the same type of for loop exceot with subtract
cont_a = 0
cont_b = 0
sub = []
for i in vector_b:
    A = float(vector_a[cont_a])
    B = float(vector_b[cont_b])
    subtract = A - B
    sub.append(subtract)
    cont_a += 1
    cont_b += 1
print(f'A - B is {sub}')
    
# For dot product create the same type of for loop
cont_a = 0
cont_b = 0
dot = 0
for i in vector_a:
    A = float(vector_a[cont_a])
    B = float(vector_b[cont_b])
    multiply = A * B
    dot += multiply
    cont_a += 1
    cont_b += 1
    
print(f'The dot product is {dot:.2f}')


# Find the magnitude for A and B 
#vector_a = ['x':'a', y, z]
#for i in len(vector_a):
   #1 mag_a = sqrt(x**2 + y**2 + z**2)


# Create a equation that adds lists

# Create an equation that performs the dot product of inputs.