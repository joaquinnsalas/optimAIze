# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Yuriy Astapov
#               Areen Bhayani
#               Joaquin Salas
#               Aaditya Srinivasan
# Section:      576
# Assignment:   LAB Topic 12: numpy
# Date:         22 Nov 2022

import numpy as np
import matplotlib as mpl

# As a team, we have gone through all required sections of the  
# tutorial, and each team member understands the material

a = np.arange(12).reshape(3, 4)
print(f'A = {a}')
print()

b = np.matrix('0 1; 2 3; 4 5; 6 7')
print(f'B = {b}')
print()

c = np.arange(6).reshape(2, 3)
print(f'C = {c}')
print()

d = a * b * c
print(f"D = {d}")
print()

d_t = d.transpose()
print(f'D^T = {d_t}')
print()

e = np.sqrt(d) / 2
print(f'E = {e}')