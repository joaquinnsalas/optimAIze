#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 08:08:41 2022

@author: joaquinsalas
"""
# TAKE INPUTS
# Take in amount paid, convert to number
paid = float(input("Input amount paid (USD): "))
# Take in amount owed, convert to number
owed = float(input("Input amount owed (USD): "))
# CALCULATE CHANGE
# Change = paid-owed x 100
change = round((paid-owed)*100) #convert to cents

# GIVE COINS THEY NEED
#Find number of quarters
# Subtract amount given from total owed
quarters = change//25
change = change-quarters*25

# Find number of dimes
# Subtract amount given from total owed
dimes = change//10
change -= dimes*10

# Find number of nickels
# Subtract amount given from total owed
nickels = change//5
change -= nickels*5

# Find number of pennies
# Subtract amount given from total owed
pennies = change//1
change -= pennies*1

# Print "quarters" if more than one
# Print "quarter" if only one
# Print nothing if there are no quarters

if quarters>1:
    print(f'You get {quarters} quarters.')
elif quarters == 1:
    print(f'You get 1 quarter.')
    