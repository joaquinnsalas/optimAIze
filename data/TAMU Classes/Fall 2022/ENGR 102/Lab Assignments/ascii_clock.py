#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 12:27:50 2022

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
# Assignment:   LAB Topic 9: ASCII clock
# Date:         25 October 2022

from math import *

#1
numIn = str(input("Enter the time: "))  #takes time input
print()
inputList = []

for i in range(len(numIn)):
  inputList.append(numIn[i:i + 1])      #puts each index from numIn into separate index in list

#2
zero0 = '000'    #each number given 5 strings for each row
zero1 = '0 0'
zero2 = '0 0'
zero3 = '0 0'
zero4 = '000'
zero = [zero0, zero1, zero2, zero3, zero4]  #each row placed in order in list specific to number

one0 = ' 1 '
one1 = '11 '
one2 = ' 1 '
one3 = ' 1 '
one4 = '111'
one = [one0, one1, one2, one3, one4]

two0 = '222'
two1 = '  2'
two2 = '222'
two3 = '2  '
two4 = '222'
two = [two0, two1, two2, two3, two4]

three0 = '333'
three1 = '  3'
three2 = '333'
three3 = '  3'
three4 = '333'
three = [three0, three1, three2, three3, three4]

fore0 = '4 4'
fore1 = '4 4'
fore2 = '444'
fore3 = '  4'
fore4 = '  4'
fore = [fore0, fore1, fore2, fore3, fore4]

five0 = '555'
five1 = '5  '
five2 = '555'
five3 = '  5'
five4 = '555'
five = [five0, five1, five2, five3, five4]

sex0 = '666'
sex1 = '6  '
sex2 = '666'
sex3 = '6 6'
sex4 = '666'
sex = [sex0, sex1, sex2, sex3, sex4]

sevn0 = '777'
sevn1 = '  7'
sevn2 = '  7'
sevn3 = '  7'
sevn4 = '  7'
sevn = [sevn0, sevn1, sevn2, sevn3, sevn4]

ate0 = '888'
ate1 = '8 8'
ate2 = '888'
ate3 = '8 8'
ate4 = '888'
ate = [ate0, ate1, ate2, ate3, ate4]

nine0 = '999'
nine1 = '9 9'
nine2 = '999'
nine3 = '  9'
nine4 = '999'
nine = [nine0, nine1, nine2, nine3, nine4]

#3
colon0 = ' '      #colon is only one without spaces before and after
colon1 = ':'
colon2 = ' '
colon3 = ':'
colon4 = ' '
colon = [colon0, colon1, colon2, colon3, colon4]

#dictionary associates each number/colon list with corresponding number as string
replacedict = {
  '0': zero,
  '1': one,
  '2': two,
  '3': three,
  '4': fore,
  '5': five,
  '6': sex,
  '7': sevn,
  '8': ate,
  '9': nine,
  ':': colon
}

#4
for i in range(5):    #goes 5 times, once for each row
  row = ""            #row variable starts empty
  for j in range(len(inputList)):      #goes through each index of inputList
    row = row + replacedict[inputList[j]][i] + " "       #takes value of inputList at each value, value is string that is used as index
    row.strip()                                          #to check dictionary, i denotes each row, dictionary returns string at
  print(row)                                             #specified i value, .strip() takes off spaces at end of rows

#Summary: prints each row of each number, goes to next line, prints next row                                                         #of each number