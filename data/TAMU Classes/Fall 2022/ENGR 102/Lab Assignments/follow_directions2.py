#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 19:12:57 2022

@author: joaquinsalas
"""

import math
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      ENGR 102 - 576
# Assignment:   THE ASSIGNMENT NUMBER (e.g. Lab 1b-2)
# Date:         25 AUGUST 2022

purpose = "This shows the evaluation of (x^2-1)/(x-1) evaluated close to x=1";
print(purpose);

myguess = 'My guess is 2';
print(myguess);

# for loop command with boundaries

def funct(x):
    # A function is a block of code which only runs when it is called.
   r = (x**2 - 1)/(x -1)
   return r
    
for y in range(1, 9):
    #A for loop is used for iterating over a sequence
    
    print(funct(1 + 0.1**y));
    
print("My guess was off a little bit.")


  

   
