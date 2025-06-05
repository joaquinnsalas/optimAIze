#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 19:48:20 2022

@author: joaquinsalas
"""

# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Yuriy Astapov
#               Areen Bhayani
#               Joaquin Salas
#               Aaditya Srinivasan
# Section:      576
# Assignment:   LAB Topic 11: passportchecker
# Date:         15 Nov 2022


#gets input from user for file
inp = input('Enter the name of the file: ')
myfile = open(inp,'r')
count = 0
lines = myfile.read()
passp = lines.split('\n\n')
#creates file for only valid passports only
valid = open('valid_passports.txt','w')
#checks throuhg all passports in the list to see if they have the letters of this in it 
for passports in passp:
    if "byr" in passports and "iyr" in passports and "eyr" in passports and "hgt" in passports and "ecl" in passports and "pid" in passports and "cid" in passports:
        count+=1
        valid.write(passports + "\n")
        valid.write("\n")
valid.close()
print(f"There are {count} valid passports")
