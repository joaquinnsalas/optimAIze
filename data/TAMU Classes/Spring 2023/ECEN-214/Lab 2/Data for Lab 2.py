import numpy as np
import matplotlib.pyplot as plt

# data points
RL = np.array([97.65, 195.9, 0.29, 0.985, 1.08, 1.18, 1.97])
VL = np.array([1.59, 1.6, 1.4, 1.62, 1.61, 1.61, 1.62])

# line of best fit
coefficients = np.polyfit(RL, VL, 1)
m = coefficients[0]
b = coefficients[1]
line = m * RL + b

# plot the data points and line of best fit
plt.plot(RL, VL, 'o', label='Data Points')
plt.plot(RL, line, label=f'Line of Best Fit: y={m:.4f}x+{b:.4f}')

# add y-intercept equation to plot
#plt.annotate(f'y = {m:.4f}x + {b:.4f}', (150, 1.63))

# set x-axis and y-axis limits
plt.xlim(0, 200)
plt.ylim(1.3, 1.675)

# add a title and axis labels
plt.title('Plot 1: Voltage vs Resistance')
plt.xlabel('Resistance (ohms)')
plt.ylabel('Voltage (V)')

# show the plot
plt.legend()
plt.show()

##### GRAPH 2

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# data points
RL = np.array([97.65, 195.9, 0.29, 0.985, 1.08, 1.18, 1.97])  # in ohms
VL = np.array([1.59, 1.6, 1.4, 1.62, 1.61, 1.61, 1.62])  # in volts

# plot data points
fig, ax = plt.subplots(figsize=(8,6))
ax.plot(RL, VL, 'bo', label='Data')

# function for linear fit
def func(x, a, b):
    return a*x + b

# fit line to data
popt, pcov = curve_fit(func, RL, VL)
a, b = popt

# plot line of best fit
x = np.linspace(0, 2, 100)
y = a*x + b
ax.plot(x, y, 'r-', label=f'Best fit line: y={a:.3f}x+{b:.3f}')

# set axes limits
ax.set_xlim([0, 2])
ax.set_ylim([1.2, 1.7])

# set axis labels
ax.set_xlabel('Load Resistance (Ohms)')
ax.set_ylabel('Voltage (V)')
ax.set_title('Voltage vs. Load Resistance')

# add legend
ax.legend()

plt.show()
