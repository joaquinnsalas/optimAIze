"""
Created on Tue Sep 13 08:52:31 2022

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
# Assignment:   LAB Topic 3: Still More Linear Interpolation
# Date:         8 September 2022
from math import *
#gives inputs for variables and assigns values to these variables
print("Enter time 1: ")
t1 = float(input(''))
print("Enter the x position of the object at time 1: ")
x1 = float(input(''))
print("Enter the y position of the object at time 1: ")
y1 = float(input(''))
print("Enter the z position of the object at time 1: ")
z1 = float(input(''))
print("Enter time 2: ")
t2 = float(input(''))
print("Enter the x position of the object at time 2: ")
x2 = float(input(''))
print("Enter the y position of the object at time 2: ")
y2 = float(input(''))
print("Enter the z position of the object at time 2: ")
z2 = float(input(''))

ti = (t2-t1)/4# gives time intervals that you add to other values
t_1 = t1 
t_2 = t_1+ ti
t_3 = t_1 + 2*ti
t_4 = t_1 + 3*ti
t_5 = t_1 + 4*ti
t = t_1
#added ":.3f" for rounding numbers for correct answers.
d_x = ((x2-x1)/(t2-t1)) * (t-t1) + x1
d_y = ((y2-y1)/(t2-t1)) * (t-t1) + y1
d_z = ((z2-z1)/(t2-t1)) * (t-t1) + z1
print(f'At time {t:.2f} seconds the object is at ({d_x:.3f},{d_y:.3f},{d_z:.3f})')
t = t_2
d_x = ((x2-x1)/(t2-t1)) * (t-t1) + x1
d_y = ((y2-y1)/(t2-t1)) * (t-t1) + y1
d_z = ((z2-z1)/(t2-t1)) * (t-t1) + z1
print(f'At time {t:.2f} seconds the object is at ({d_x:.3f},{d_y:.3f},{d_z:.3f})')
t = t_3
d_x = ((x2-x1)/(t2-t1)) * (t-t1) + x1
d_y = ((y2-y1)/(t2-t1)) * (t-t1) + y1
d_z = ((z2-z1)/(t2-t1)) * (t-t1) + z1
print(f'At time {t:.2f} seconds the object is at ({d_x:.3f},{d_y:.3f},{d_z:.3f})')
t = t_4
d_x = ((x2-x1)/(t2-t1)) * (t-t1) + x1
d_y = ((y2-y1)/(t2-t1)) * (t-t1) + y1
d_z = ((z2-z1)/(t2-t1)) * (t-t1) + z1
print(f'At time {t:.2f} seconds the object is at ({d_x:.3f},{d_y:.3f},{d_z:.3f})')
t = t_5
d_x = ((x2-x1)/(t2-t1)) * (t-t1) + x1
d_y = ((y2-y1)/(t2-t1)) * (t-t1) + y1
d_z = ((z2-z1)/(t2-t1)) * (t-t1) + z1
print(f'At time {t:.2f} seconds the object is at ({d_x:.3f},{d_y:.3f},{d_z:.3f})')


