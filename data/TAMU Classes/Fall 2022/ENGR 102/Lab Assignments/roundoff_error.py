"""
Created on Tue Sep 20 15:23:00 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Joaquin Salas
# Section:      576
# Assignment:   LAB Topic 4: Roundoff Error
# Date:         20 September 2022

############ Part A ############
a = 1 / 7
print(f'a = {a}')
b = a * 7
print(f'b = a * 7 = {b}')

# Since there is a division symbol, pyhton will turn the number
# into a float or decimal number, when you multiply,  python wont
# turn the number into a float.

c = 2 * a
d = 5 * a
f = c + d
print(f'f = 2 * a + 5 * a = {f}')

# The number is not "1.", it is actually "0.9999..."
# This contradicts my previous answer where I stated
# that the only reason that the number was a decimal
# was because of the division, but it seems like the 
# exact same thing is happening with the multiplication.

from math import sqrt
x = sqrt(1 / 3)
print(f'x = {x}')
y = x * x * 3
print(f'y = x * x * 3 = {y}')
z = x * 3 * x
print(f'z = x * 3 * x = {z}')

# In these lines of code, if the order is "y = x * x * 3"
# python prints a "1.0",  if the order is "z = x * 3 * x"
# python prints a ".9999...". This is confusinga as to
# why this happens, but after researching this, it is
# because of floating numbers when python runs using its
# binary digits to represent a decimal number. This is 
# difficult to represent which leads to little roundoff 
# errors.

############ Part B ############

TOL = 1e-10
# check if b and f are equal within specified tolerance
if abs(b - f) < TOL:
    print(f'b and f are equal within tolerance of {TOL}')
else:
    print(f'b and f are NOT equal within tolerance of {TOL}')
    
TOL = 1e-10
# check if y and z are equal within specified tolerance
if abs(y - z) < TOL:
    print(f'y and z are equal within tolerance of {TOL}')
else:
    print(f'y and z are NOT equal within tolerance of {TOL}')
    
############ Part C ############

m = 0.1
print(f'm = {m}')
n = 3 * m
print(f'n = 3 * m = 0.3 {n==0.3}')
p = 7 * m
print(f'p = 7 * m = 0.7 {p==0.7}')
q = n + p
print(f'q = n + p = 1 {q==1}')








