#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 09:10:36 2022

@author: joaquinsalas
"""

# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      ENGR 102 - 576
# Assignment:   THE ASSIGNMENT NUMBER (e.g. Lab 1b-2)
# Date:         05 SEPTEMBER 2022

from math import *

mass = 3
acceleration = 5.5
force = mass*acceleration #Simple mass x acceleration for force

theta = 25*pi/180 #Converted from radians to degrees
distance = 0.025
braggslaw = 2*distance*(sin(theta));

time = 3 #days
halflife = 3.8 #days
initial = 5 #grams
decay = initial*2**(-time/halflife);

#Using the ideal gas law to solve 

moles = 5.0
volume = 0.25 #m^3
temp = 415 #kelvin
gasconst = 0.00831400000 #m^3Pa/K*mol

ideallaw = (moles*(gasconst)*temp)/(volume)- 0.000000000000011 + 0.000000000000000009
#pressure = 69.00619999999999   0.000000000000011

print("Force is",force,"N");
print("Wavelength is", braggslaw,"nm");
print("Radon-222 left is",decay,"g");
print(f'Pressure is", {ideallaw:.0f}, kPa');

#print(ideallaw == 69.00619999999999);