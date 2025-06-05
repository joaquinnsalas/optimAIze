"""
Created on Fri Oct 14 18:00:39 2022

@author: joaquinsalas
"""
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
# Names:        Joaquin Salas
# Section:      576
# Assignment:   LAB Topic 7: pig_latin.py
# Date:         18 October 2022
#get a string by user input
inptword = input('Enter word(s) to convert to Pig Latin: ')

#convert the string into a list
li = list(inptword.split(" "))
newli = list()
seperator = " "
#check the first letter with the vowels or constants
# if the first letter is a vowel including 'y' add 'yay' to the end
# a for loop in range of the list, convert 
for i in range(len(li)):
  word = li[i]
  if word[0:1] in ['a', 'e', 'i', 'o', 'u', 'y']:
    pig = word + 'yay'
    newli.append(pig)
# if its a cluster, move cluster to the end of the word
# and append 'ay'
  elif word[0:3] in ['sch', 'shr', 'spl', 'squ', 'thr', 'spr', 'scr', 'sph']:
    pig = word[3:] + word[0:3] + "ay"
    newli.append(pig)
# if it's a consonant then move consonant to end of the word
# and append 'ay'
  elif word[0:2] in ['bl', 'cl', 'fl', 'gl', 'pl', 'sl', 'br', 'cr', 'dr', 'fr', 'gr', 'pr', 'tr', 'sc', 'sk', 'sm', 'sn', 'sp', 'st', 'sw', 'tw', 'wh', 'ch', 'th', 'wr']:
    pig = word[2:] + word[0:2] + "ay"
    newli.append(pig)
  else:
    pig = word[1:] + word[0] + "ay"
    newli.append(pig)
print(f'In Pig Latin, "{inptword}" is: {seperator.join(newli)}')
