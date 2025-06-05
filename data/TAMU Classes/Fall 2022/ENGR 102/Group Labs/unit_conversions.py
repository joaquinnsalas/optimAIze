"""
Created on Mon Sep 12 15:48:19 2022

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
# Assignment:   LAB Topic 3: Unit Conversions
# Date:         8 September 2022
from math import *
print('Please enter the quantity to be converted: ')
quan = float(input(''))
newtons = 4.44822 * quan #1 pound = 4.44822 watts
ft = 3.28084 * quan #1 meter = 3.28084 feet
kPa = 101.325 * quan #1 atmosphere = 101.325 kPa
btu = 3.412141633 * quan #1 watt = 3.412141633 BTU
Gal = quan * 0.264172052 * 60 #1 L/sec = 15.8503 gallons/min
Far = quan*1.8 + 32 #farenheit = cel(1.8) + 32

print(f'{quan:.2f} pounds force is equivalent to {newtons:.2f} Newtons')
print(f'{quan:.2f} meters is equivalent to {ft:.2f} feet')
print(f'{quan:.2f} atmospheres is equivalent to {kPa:.2f} kilopascals')
print(f'{quan:.2f} watts is equivalent to {btu:.2f} BTU per hour')
print(f'{quan:.2f} liters per second  is equivalent to {Gal:.2f} US gallons per minute')
print(f'{quan:.2f} degrees Celsius is equivalent to {Far:.2f} degrees Fahrenheit')
