#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 18:35:51 2022

@author: joaquinsalas
"""

# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      ENGR 102 - 576
# Assignment:   Lab 2.10
# Date:         07 SEPTEMBER 2022

from math import * #To import math function library
from sympy import *
import math

#Same equation from linear interpolation formula, just in a 3rd dimension so repeat 3 times

tinitial = 12
tfinal = 85
xinitial = 8
yinitial = 6
zinitial = 7
xfinal = -5
yfinal = 30
zfinal = 9

#Distance at time t
t1 = 30.0
t2 = 37.5
t3 = 45.0
t4 = 52.5
t5 = 60.0

x1 = ((xfinal - xinitial)/(tfinal - tinitial)) * (t1 - tinitial) + xinitial
y1 = ((yfinal - yinitial)/(tfinal - tinitial)) * (t1 - tinitial) + yinitial
z1 = ((zfinal - zinitial)/(tfinal - tinitial)) * (t1 - tinitial) + zinitial

print("At time", t1, 'seconds:')
print("x1 =", x1, "m")
print("y1 =", y1, "m")
print("z1 =", z1, "m")
print('-----------------------');

x2 = ((xfinal - xinitial)/(tfinal - tinitial)) * (t2 - tinitial) + xinitial
y2 = ((yfinal - yinitial)/(tfinal - tinitial)) * (t2 - tinitial) + yinitial
z2 = ((zfinal - zinitial)/(tfinal - tinitial)) * (t2 - tinitial) + zinitial

print("At time", t2, 'seconds:')
print("x2 =", x2, "m")
print("y2 =", y2, "m")
print("z2 =", z2, "m")
print('-----------------------');

x3 = ((xfinal - xinitial)/(tfinal - tinitial)) * (t3 - tinitial) + xinitial
y3 = ((yfinal - yinitial)/(tfinal - tinitial)) * (t3 - tinitial) + yinitial
z3 = ((zfinal - zinitial)/(tfinal - tinitial)) * (t3 - tinitial) + zinitial

print("At time", t3, 'seconds:')
print("x3 =", x3, "m")
print("y3 =", y3, "m")
print("z3 =", z3, "m")
print('-----------------------');

x4 = ((xfinal - xinitial)/(tfinal - tinitial)) * (t4 - tinitial) + xinitial
y4 = ((yfinal - yinitial)/(tfinal - tinitial)) * (t4 - tinitial) + yinitial
z4 = ((zfinal - zinitial)/(tfinal - tinitial)) * (t4 - tinitial) + zinitial

print("At time", t4, 'seconds:')
print("x4 =", x4, "m")
print("y4 =", y4, "m")
print("z4 =", z4, "m")
print('-----------------------');

x5 = ((xfinal - xinitial)/(tfinal - tinitial)) * (t5 - tinitial) + xinitial
y5 = ((yfinal - yinitial)/(tfinal - tinitial)) * (t5 - tinitial) + yinitial
z5 = ((zfinal - zinitial)/(tfinal - tinitial)) * (t5 - tinitial) + zinitial

print("At time", t5, 'seconds:')
print("x5 =", x5, "m")
print("y5 =", y5, "m")
print("z5 =", z5, "m")
