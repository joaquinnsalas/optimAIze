"""
Created on Sun Oct  2 22:55:18 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Joaquin Salas
# Section:      576
# Assignment:   LAB Topic 5: Boiling Curve
# Date:         03 October 2022
from math import *

# First allow the user to input a variable named the excess temperature

excesstemp = float(input('Enter the excess temperature: '))
# Next my program will calculate the surface heat flux to 4 sig figs
# To find surface heat flux I need the following equation
# And i need to set up an if statement for temperatures less than 0
if excesstemp < 0:
    print(f'Surface heat flux is not available')

# Now create an elif statement for if the temperature is between points A and C 
# Using the equation provided I will solve for m with points A and B and than I will 
# plug in the Slope M into the Heat flux formula that we were also given 

elif 1.3 <= excesstemp < 5:
    
    m = (log10(7000 / 1000)) / (log10(5 / 1.3))
    heatflux = 1000 * ((excesstemp / 1.3)**m)
    print(f'The surface heat flux is approximately {heatflux:.0f} W/m^2')
    
# Now create in elif statement for if the temperature is between points B to C 

elif 5 <= excesstemp < 30:
    
    m = (log10((1.5 * 10**6) / 7000)) / (log10(30 / 5))
    heatflux = 7000 * ((excesstemp / 5)**m)
    print(f'The surface heat flux is approximately {heatflux:.0f} W/m^2')
    
# Now im going to create another elif statement to calculate the heat flux when
# Excess temperature is between points C and D on the graph. 

elif 30 <= excesstemp < 120:
    
    m = (log10((2.5 * 10**4) / (1.5 * 10**6))) / (log10(120 / 30))
    heatflux = (1.5 * 10**6) * ((excesstemp / 30)**m)
    print(f'The surface heat flux is approximately {heatflux:.0f} W/m^2')
    
# Now im going to create another elif statement to calculate the heat flux when
# Excess temperature is between points D and E on the graph. 

elif 120 <= excesstemp < 1200:
    
    m = (log10((1.5 * 10**6) / (2.5 * 10**4))) / (log10(1200 / 120))
    heatflux = (2.5 * 10**4) * ((excesstemp / 120)**m)
    print(f'The surface heat flux is approximately {heatflux:.0f} W/m^2')
    
# Now im going to create an else statement after all my elif statements to print that 
# a result is not available for any excess temperature greater than 1200

else:
    print(f'Surface heat flux is not available')

