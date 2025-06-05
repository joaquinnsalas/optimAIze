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

print("This program calculates the applied force given mass and acceleration")

print("Please enter the mass (kg): ")
mass = float(input(''))

print("Please enter the acceleration (m/s^2): ")
acceleration = float(input(''))

#mass = 3
#acceleration = 5.5
force = mass*acceleration #Simple mass x acceleration for force

print(f'Force is {force:.1f} N')

print(' ')


#I will convert all print statements into f strings


print('This program calculates the wavelength given distance and angle')

print("Please enter the distance (nm): ")
distance = float(input(''))

print("Please enter the angle (degrees): ")
theta = float(input(''))  #Converted from radians to degrees

#theta = 25*pi/180 #Converted from radians to degrees
#distance = 0.025
braggslaw = 2*distance*(sin(theta*(pi/180.0)));

print(f'Wavelength is {braggslaw:.4f} nm')

print(' ')




print('This program calculates how much Radon-222 is left given time and initial amount')

print("Please enter the time (days): ")
time = float(input(''))

print("Please enter the initial amount (g): ")
initial = float(input(''))

#time = 3 #days
halflife = 3.8 #days
#initial = 5 #grams
decay = initial*2**(-time/halflife);

print(f'Radon-222 left is {decay:.2f} g')

print(' ')





print('This program calculates the pressure given moles, volume, and temperature')

print("Please enter the number of moles: ")
moles = float(input(''))

print("Please enter the volume (m^3): ")
volume = float(input(''))

print("Please enter the temperature (K): ")
temp = float(input(''))


#moles = 5
#volume = 0.25 #m^3
#temp = 415 #kelvin
gasconst = 8.314 #m^3Pa/K*mol

ideallaw = (moles*(gasconst)*temp)/(volume)*(1/1000)

print(f'Pressure is {ideallaw:.0f} kPa');