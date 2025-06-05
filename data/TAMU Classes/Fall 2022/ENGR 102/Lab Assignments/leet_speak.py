#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 08:38:47 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Joaquin Salas
# Section:      576
# Assignment:   LAB Topic 7: leet_speak.py
# Date:         18 October 2022
# Im going to start by creating a dictionary
# And getting a users input:
text = input('Enter some text: ')
original = text
#Create a dictionary to use in the code.
convert = {'a':'4', 'e':'3', 'o':'0', 's':'5', 't':'7'}
# Now make a for loop to loop through every word in the string
# and find a word to change with the other.

for j in text:
    if 'a' in text:
        text = text.replace('a', '4') # using text.replace to switch letters
    elif 'e' in text:
        text = text.replace('e', '3')
    elif 'o' in text:
        text = text.replace('o', '0')
    elif 's' in text:
        text = text.replace('s', '5')
    elif 't' in text:
        text = text.replace('t', '7')
    else:
        break
    
print(f'In leet speak, "{original}" is: ')
print(text)


     
