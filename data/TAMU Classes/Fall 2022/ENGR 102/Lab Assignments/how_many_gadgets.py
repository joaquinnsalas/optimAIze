"""
Created on Thu Sep 22 20:52:05 2022

@author: joaquinsalas
"""
from math import *


day = int(input('Please enter a positive value for day: '))

if day < 0:
    print(f'You entered an invalid number!')
# First 10 days it is producing 10 units
elif day <= 10:
    print(f'The total number of gadgets produced on day {day} is 15')
# From days 11 to 60 it is producing 50 units
elif day <= 60:
    print(f'The total number of gadgets produced on day {day} is 300')
elif day <= 101:
    amount = int((-(1/2))*day + 80)
    print(f'The total number of gadgets produced on day {day} is {amount}')
elif day >= 102:
    print(f'The total number of gadgets produced on day {day} is 3730')

