"""
Created on Sat Sep 24 16:49:32 2022

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
# Assignment:   LAB Topic 5: Diabetes Risk
# Date:         27 September 2022
from math import *
# Start by getting the user to input all needed data
# get input of sex and set it to sex variable
sex = input('Enter your sex (M/F): ')
# get input of age and set it to sex age

age = int(input('Enter your age (years): '))
bmi = float(input('Enter your BMI: '))
meds = input('Are you on medication for hypertension (Y/N)? ')
steroids = input('Are you on steroids (Y/N)? ')
smoke = input('Do you smoke cigarettes (Y/N)? ')
# get input of did you smoke and set it to smoke variable
# get input did you used to smoke and set it to pastsmoke variable
if smoke == 'N' or smoke == 'n':
  pastsmoke = input('Did you used to smoke (Y/N)? ')
  if (pastsmoke == "Y" or pastsmoke == "y"):
    gsmoke = -0.218
  if (pastsmoke == "N" or pastsmoke == "n"):
    gsmoke = 0
fdiabetes = input('Do you have a family history of diabetes (Y/N)? ')
if fdiabetes == 'Y' or fdiabetes == 'y':
  family = input('Both parent and sibling (Y/N)? ')
  if family == 'Y' or family == 'y':
    gdiabetes = 0.753
  if family == 'N' or family == 'n':
    gdiabetes = 0.728
if sex == 'M' or sex =='m':
  gsex = 0
if sex == 'F' or sex =='f':
  gsex = 0.879
# get input of BMI and set it to sex BMI
if bmi < 25:
  gbmi = 0
elif bmi >= 25 and bmi < 27.5:
  gbmi = 0.699
elif bmi >= 27.5 and bmi < 30:
  gbmi = 1.97
elif bmi >= 30:
  gbmi = 2.518
# get input of medication  and set it to medication variable
if meds == "Y" or meds == "y":
  gmeds = 1.222
elif meds =="N" or meds == "n":
  gmeds = 0
# get input of steroids and set it to steriods variable
if steroids == "Y" or steroids == "y":
  gster = 2.191
elif steroids == "N" or steroids == "n":
  gster = 0

if smoke == "Y" or smoke == "y":
  gsmoke = 0.855
if fdiabetes == 'N' or fdiabetes == 'n':
  gdiabetes = 0
  
n = 6.322 + gsex - (0.063 * age) -gbmi - gmeds - gster - gsmoke - gdiabetes

risk = (100 / (1 + e**n))

print(f'Your risk of developing type-2 diabetes is {risk:.1f}% ')

# Start by getting the user to input all needed data
# get input of sex and set it to sex variable
# get input of age and set it to sex age
# get input of BMI and set it to sex BMI
# get input of medication  and set it to medication variable
# get input of steroids and set it to steriods variable
# get input of did you smoke and set it to smoke variable
# get input did you used to smoke and set it to pastsmoke variable

# create if statement that is equal to F or f and then in the if loop create another variable

# create an if statement for BMI that splits up ranges, under 25:0, 25 to 27.49: 0.699, 27.5 to 29.99: 1.97, ≥30: 2.518 

# create an if statement for on meds or not on meds,
# On meds: 1.222 or Not on meds: 0 

# create an if statement for on steroids or not on steroids,
# On meds: 2.191 or Not on meds: 0 

# create and if statement for smoker or past smoker
# Non-smoker: 0 , Used to smoke: -0.218 , Smoker: 0.855 

# create and if statement for family history or no family history
# None: 0 , Parent or sibling: 0.728, Parent and sibling: 0.753

# Make equation to calculate "n" and than calculate risk.

