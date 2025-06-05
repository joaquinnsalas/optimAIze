"""
Created on Tue Sep 20 13:31:48 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Joaquin Salas
# Section:      576
# Assignment:   LAB Topic 4: Largest Number
# Date:         20 September 2022

# Starting by allowing user to input numbers, they can even be decimals
num_1 = float(input("Enter number 1: "))
num_2 = float(input("Enter number 2: "))
num_3 = float(input("Enter number 3: "))

# If number 1 is greater than 2 and 3, it is the largest number
if (num_1 > num_2) and (num_1 > num_3) :
    print(f'The largest number is {num_1}')
elif (num_1 == num_2):
    print(f'The largest number is {num_1}')
elif (num_1 == num_3):
    print(f'The largest number is {num_1}')
        
        
# If number 2 is greater than 1 and 3, it is the largest number
if (num_2 > num_1) and (num_2 > num_3) :
    print(f'The largest number is {num_2}')
elif (num_2 == num_3):
    print(f'The largest number is {num_2}')

    
# If number 3 is greater than 1 and 2, it is the largest number
if (num_3 > num_2) and (num_3 > num_1) :
    print(f'The largest number is {num_3}')
