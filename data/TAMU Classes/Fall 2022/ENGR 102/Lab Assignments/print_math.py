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
# Date:         25 AUGUST 2022

from math import *

force = 3*5.5

print("Force is",force,"N");

#Calculate the wavelength of x-rays scattering from a crystal lattice with a distance between
#crystal layers of 0.025 nm, scattering angle of 25 degrees, and first order diffraction.
#Bragg’s Law describes the scattering of waves from a crystal using the equation
#nλ = 2d sin θ The standard unit of wavelength in the SI system is nanometers (nm).

equation = 2*0.025*(sin(25*pi/180));

print("Wavelength is", equation,"nm");

decay = 5*2**(-3/3.8);

print("Radon-222 left is",decay,"g");

#pressure = (5*(8.314*10**-3)*415)/(0.25)
pressure = 69.00619999999999

print("Pressure is", pressure,"kPa");
