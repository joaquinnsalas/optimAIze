# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      ENGR 102 - 576
# Assignment:   THE ASSIGNMENT NUMBER (e.g. Lab 1b-2)
# Date:         15 SEPTEMBER 2022

from math import *

def printresult(shape, side, area):
    '''Print the result of the calculation'''
    print(f'A {shape} with side {side:.2f} has area {area:.3f}')


# example function call:
# printresult(<string of shape name>, <float of side>, <float of area>)
# printresult('square', 2.236, 5)
# Your code goes here

print('Please enter the side length: ')
length = float(input(''))
areatriangle = (sqrt(3)/4)*length**2
printresult('triangle', length, areatriangle);
#make equations for each of the shapes to find area
#useprint result since it was in the code provided
areasquare = length**2
printresult('square', length, areasquare)


areapentagon = (1/4)*sqrt(25+(10*sqrt(5)))*length**2
printresult("pentagon", length, areapentagon)


areadode = 3*(2+sqrt(3))*length**2
printresult('dodecagon', length, areadode)

