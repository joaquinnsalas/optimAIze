"""
Created on Thu Oct  6 07:57:21 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Joaquin Salas
# Section:      576
# Assignment:   LAB Topic 6: Howdy whoop
# Date:         27 September 2022


# First start by letting the user input an int.
intone = int(input('Enter an integer: '))
inttwo = int(input('Enter another integer: '))
# Set i
i = 0

# If # is evenly divisible by 1 or i 
#for i in range(1,101):
for i in range (100):
    i += 1
    # For first condition
    if i % intone != 0 and i % inttwo != 0:
        print(i)
    # If the number is evenly divisible by the first integer, print Howdy.
    elif i % intone == 0 and i % inttwo != 0:
        print('Howdy')
    # If divisible by second integer print whoop
    elif i % intone != 0 and i % inttwo == 0:
        print('Whoop')
    
    else:
        print('Howdy Whoop')

    
    
