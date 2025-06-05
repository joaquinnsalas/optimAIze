import matplotlib.pyplot as plt
import numpy as np

# Data
resistor_values = [0, 100, 1000, 10000, 100000];
voltage_values = [9.00, 8.99, 9.00, 9.00, 9.00];

# Plotting data as a scatter plot
plt.scatter(resistor_values, voltage_values, color='blue');

# line connecting all the data points
plt.plot(resistor_values, voltage_values, 'r-', linewidth=2);

# Labeling plot
plt.title("Resistors vs. Voltage");
plt.xlabel("Resistor Values (Ohms)");
plt.ylabel("Voltage Values (Volts)");

# Adding gridlines
plt.grid(True, linestyle='--');

# y-axis limit
plt.ylim(8, 10);

# plot
plt.show();

#####################################################################

# Low Voltage (1.5 Volts)
lower_resistors = [100, 1000, 10000, 100000];
lower_voltage = [88e-3, 0.58, 1.34, 1.5];

# High Voltage (5 Volts)
high_resistors = [100, 1000, 10000, 100000];
high_voltage = [0.5, 2.6, 4.5, 4.9];

# Plot the data
plt.plot(lower_resistors, lower_voltage, label='Lower Voltage (1.5 Volts)', marker='o', color= 'blue');
plt.plot(high_resistors, high_voltage,'r-', label='High Voltage (5 Volts)', marker='o');

# axis labels and title
plt.xlabel('Resistor Value (Ohms)');
plt.ylabel('Voltage (Volts)');
plt.title('Graph 2: Task 1 Data Results');

# legend, grid, and plot
plt.legend();
plt.grid();
plt.show();

#####################################################################

# low voltage
resistor_values_low = [100, 1000, 10000, 100000];
voltage_values_low = [0.17, 1.3, 5.0, 4.87];

# high voltage
resistor_values_high = [100, 1000, 10000, 100000];
voltage_values_high = [0.16, 0.84, 1.45, 1.5];

# Plot the data
plt.plot(lower_resistors, lower_voltage, label='Lower Voltage (1.5 Volts)', marker='o', color = 'blue');
plt.plot(high_resistors, high_voltage, 'r-', label='High Voltage (5 Volts)', marker='o');

# axis labels and title
plt.xlabel('Resistor Value (Ohms)');
plt.ylabel('Voltage (Volts)');
plt.title('Graph 3: Resistor 1 as Variable Resistor and Resistor 2 Fixed Resistor');

# gridlines
plt.grid(True, linestyle='--');

# legend
plt.legend();

# plot
plt.show();

#####################################################################

# Low Voltage
lower_resistors = [100, 1000, 10000, 100000];
lower_voltage = [0.20, 1.5, 4.0, 4.9];

# High Voltage
high_resistors = [100, 1000, 10000, 100000];
high_voltage = [0.1, 0.6, 1.3, 1.5];

# Plot the data
plt.plot(lower_resistors, lower_voltage, label='Lower Voltage (1.5 Volts)', marker='o', color = 'blue');
plt.plot(high_resistors, high_voltage, 'r-', label='High Voltage (5 Volts)', marker='o');

# axis labels and title
plt.xlabel('Resistor Value (Ohms)');
plt.ylabel('Voltage (Volts)');
plt.title('Graph 4: Resistor 1 and Resistor 2 as Variable Resistor');

# gridlines
plt.grid(True, linestyle='--');

# legend
plt.legend();

# plot
plt.show();