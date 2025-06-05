# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      576
# Assignment:   Lab 12.16 Pretty Plot
# Date:         29 November 2022


import numpy as np
import matplotlib.pyplot as plt

M = np.array([[1.01, -0.09], [0.09, 1.01]]) #first take the vectors
p = np.array([[0,1]])
v = p.transpose()
x = np.array([1])
y = np.array([0])
for i in range(0,250):
    c = np.dot(M,v)
    x = np.append(x, c[0][0]) #plot this data
    y = np.append(y, c[1][0]) 
    v=c
plt.plot(x, y, 'r--') 
plt.xlabel('X') 
plt.ylabel('Y') 
plt.title('Trace out') 
plt.show()
