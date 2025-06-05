"""
Created on Tue Oct  4 09:39:13 2022

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
# Assignment:   LAB Topic 6: Pyramid Area Part 1
# Date:         29 September 2022
from math import *
#take input of length and layers
len = float(input('Enter the side length in meters: '))
layers = int(input('Enter the number of layers: '))
prisms = 0
gold = 0
temp = 0 
for i in range(layers+1):
  A = (sqrt(3)/4)*((len*i)**2)
  SA = 3*len*(len*i) + A - temp
  temp = A
  gold += SA
print(f'You need {gold:.2f} m^2 of gold foil to cover the pyramid')  