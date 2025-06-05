"""
Created on Thu Sep 22 09:22:20 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Joaquin Salas
# Section:      576
# Assignment:   LAB Topic 4.19
# Date:         22 September 2022
from math import *
a = float(input('Please enter the coefficient A: '))
b = float(input('Please enter the coefficient B: '))
c = float(input('Please enter the coefficient C: '))
# First input the discriminant, this will help me tell which
# equations will have how many roots.

discriminant = (b**2) - (4*a*c)
#First if a and b are 0, no solution is possible so let the 
# person know
if a == 0 and b == 0:
    print('You entered an invalid combination of coefficients!')
# If a = 0, there will only be one root since the eq will be bx + c
# so this is a simple equation
elif a == 0:
    one_root = (-c / b)
    print(f'The root is x = {one_root}')
# If discriminant is greater than 0 , there will be 2 roots, we can use the
# quadratic formula to solve for these.
elif discriminant > 0:
    tworoots1 = (-b + sqrt(b**2 - 4 * a * c))/(2 * a)
    tworoots2 = (-b - sqrt(b**2 - 4 * a * c))/(2 * a)
    print(f'The roots are x = {tworoots1} and x = {tworoots2}')
# If the discriminant = 0 the equation is simply
# -b/2a
elif discriminant == 0:
    root1 = (-b / 2 * a)
    print(f'The root is x = {root1}')
# Figure out what happens if discriminant is less than 0
elif discriminant < 0 :
    a1 = (-b / 2 * a)
    a2 = (-b / 2 * a)
    b1 = (b**2) - (4*a*c)**0.5
    b2 = - (b**2) - (4*a*c)**0.5
    imagn1 = abs(b1)/2 * a // 5
    imagn2 = abs(b2)/2 * a // 10
    print(f'The roots are x = {a1} + {imagn1:.1f}i and x = {a2} - {imagn2:.1f}i')