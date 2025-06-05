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

# tutorial, and each team member understands the material
# As a team, we have gone through all required sections of the
# tutorial, and each team member understands the material
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# As a team, we have gone through all required sections of the
# tutorial, and each team member understands the material

###### FIRST GRAPH ########
f1 = 2
x = np.linspace(-2.0, 2.0, 100)
y1 = (1/(4*f1))*(x**2)
f2 = 6
y2 = (1/(4*f2))*(x**2)

plt.plot(x, y1, "r", linewidth = "2", label = "f=2")
plt.plot(x, y2, "b", linewidth = "6", label = "f=6")
plt.suptitle('Parabola plots with varying focal length')
plt.ylabel('y')
plt.xlabel('x')
plt.show()

###### SECOND GRAPH #######
#a = 2
#b = 3
#c = 11
#d = 6
#graph = np.linspace(-4.0, 4.0, 125)
x = np.linspace(-4, 4, 25)
y = 2*(x**3) + 3*(x**2) - 11*x - 6
plt.plot(x,y,'*')
plt.suptitle('Plot of cubic polynomial')
plt.ylabel('y values')
plt.xlabel('x values')
plt.show()



###### THIRD GRAPH ########

x = np.arange(-2 * np.pi, 2 * np.pi, 0.1)
#y1 = np.sin(2*np.pi * x)
y1 = np.sin(x)


x = np.arange(-2 * np.pi, 2 * np.pi, 0.1)
y2 = np.cos(x)


fig, (ax1,ax2) = plt.subplots(2, sharex = True)
fig.suptitle('Plot of cos(x) and six(x)')
ax1.plot(x, y2, 'r', lw = 1)
ax2.plot(x, y1, 'b', lw = 2)
ax1.ylabel('y=cos(x)')
ax2.ylabel('y=sin(x)')
ax1.grid(True)
ax2.legend(['sin(x)'])
ax1.legend(['cos(x)'])
ax2.grid(True)
fig.show()

