"""
Created on Tue Sep 20 08:04:18 2022

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
# Assignment:   LAB Topic 4: Make Change
# Date:         15 September 2022
from math import *

#first create input available for how much the customer paid and how #much the item cost.

print("How much did you pay?")
pay = float(input(''))
print("How much did it cost?")
cost = float(input(''))
#Convert the inputs into floats to allow python to run the code
change = pay - cost
#Set up a f statement to print text with inputs
quar = 0
dimes = 0
nickels = 0
pennies = 0
print(f'You received ${change:.2f} in change. That is...')
if change >= .25:
  quar = int(change /.25)
  change %= 0.25
  change = round(change,2)
  
  #print(f'{quar} quarters')
  if change >= .10:
    dimes = int(change/.10)
    change %= .10
    change = round(change,2)
    #print(f'{dimes} dimes')
    if change >= .05:
      nickels = int(change/.05)
      change %=.05
      change = round(change,2)
      #print(f'{nickels} nickles')
      if change >=.01:
        change = round(change,2)
        pennies = int(change/.01)
        change %=.01
        
        #print(f'{pennies} pennies')
elif change >= .10:
  dimes = int(change/.10)
  change %= .10
  change = round(change,2)
  #print(f'{dimes} dimes')
  if change >= .05:
    nickels = int(change/.05)
    change %=.05
    change = round(change,2)
    #print(f'{nickels} nickles')
    if change >=.01:
      change = round(change,2)
      pennies = int(change/.01)
      change %=.01
      
      #print(f'{pennies} pennies')
if change >= .05:
  nickels = int(change/.05)
  change %=.05
  change = round(change,2)
  #print(f'{nickels} nickels')
  if change >=.01:
    change = round(change,2)
    pennies = int(change/.01)
    change %=.01
    
    #print(f'{pennies} pennies')
else:
  change = round(change,2)
  pennies = round(int(change/.01),0)
  #print(f'{pennies} pennies')


if quar > 1:
  print(f'{quar} quarters')
elif quar == 1:
  print(f'{quar} quarter')
if dimes > 1:
  print(f'{dimes} dimes')
elif dimes == 1:
  print(f'{dimes} dime')
if nickels > 1:
  print(f'{nickels} nickels')
elif nickels == 1:
  print(f'{nickels} nickel')
if pennies > 1:
  print(f'{pennies} pennies')
elif pennies == 1:
  print(f'{pennies} penny')


#print(f'{dimes} dimes')
#print(f'{nickles} nickles')
#print(f'{pennies} pennies')
