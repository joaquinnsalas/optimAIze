"""
Created on Thu Oct  6 23:17:30 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Joaquin Salas
# Section:      576
# Assignment:   LAB Topic 6: Juggler Sequence
# Date:         07 October 2022
from math import *

# Let the user input a integer and make it positive
n = int(input('Enter a positive integer: '))
print(f'The Juggler sequence starting at {n} is:')

i = 0
while n != 1:
        print(f'{n},', end ='')
        # If number is even make it floor
        if n % 2 == 0:
            n = int(sqrt(n))
            i = i + 1
        # If number is not even, make it the floor for **3/2
        else:
            i = i + 1
            n = int(n ** (3/2))
    # print the list that is given
print(n)
   
#print(f'The Juggler sequence starting at {n} is:')
print(f'It took {i} iterations to reach 1')
