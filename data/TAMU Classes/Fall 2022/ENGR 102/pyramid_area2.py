"""
Created on Tue Oct  4 09:40:39 2022

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
# Assignment:   LAB Topic 6: Pyramid Area Part 2
# Date:         4 October 2022
from math import *
#take input of length and layers
len = float(input('Enter the side length in meters: '))
layers = int(input('Enter the number of layers: '))
#arthmetic progression
a1 = 1
n = layers
d = 1
#area of the entire base 
A = (sqrt(3)/4)*((len*layers)**2)
#should give number of trianges
sum = (n/2)*((2*a1)+(n-1)*d)
gold = 3*sum*(len**2) + A
print(f'You need {gold:.2f} m^2 of gold foil to cover the pyramid')  
