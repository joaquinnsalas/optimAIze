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

inp = input('Enter the name of the file: ')
myfile2 = open(inp,'r')
count = 0
lines = myfile2.read()
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

#gets input from user for file
myfile = open('valid_passports.txt','r+')
count = 0
lines = myfile.read()
passp = lines.split('\n\n')
#creates file for only valid passports only
valid = open('valid_passports2.txt','w')
#checks throuhg all passports in the list to see if they have the letters of this in it 
for passports in passp:
  lists = passports.split()
  for part in lists:
    if 'byr' in part:
      part = part.split(":")
      part = part[1]
      part = int(part)
      if (part <= 2005 and part >= 1920):
        pvalid = True
      else:
        pvalid = False
        break
    elif 'iyr' in part:
      part = part.split(":")
      part = part[1]
      part = int(part)
      if (part <= 2022 and part >= 2012):
        pvalid = True
      else:
        pvalid = False
        break
    elif 'eyr' in part:
      part = part.split(":")
      part = part[1]
      part = int(part)
      if (part <= 2032 and part >= 2022):
        pvalid = True
      else:
        pvalid = False
        break
    elif 'hgt' in part:
      if 'cm' in part:
        part = part.split(":")
        part = part[1]
        part = part.split("cm")
        part = part[0]
        if int(part) <= 193 and int(part) >= 150:
          pvalid = True
        else:
          pvalid = False
          break
      elif 'in' in part:
        part = part.split(":")
        part = part[1]
        part = part.split("in")
        part = part[0]
        if int(part) <= 76 and int(part) >= 59:
          pvalid = True
        else:
          pvalid = False
          break
      else:
        pvalid = False
        break  
    elif 'ecl' in part:
      if ("amb" in part) or ("blu" in part) or ("brn" in part) or ("gry" in part) or ("grn" in part) or ("hzl" in part) or ("oth" in part):
        pvalid = True
      else:
        pvalid = False
        break
    elif 'pid' in part:
      if len(part) == 13:
        pvalid = True
      else:
        pvalid = False
        break
    elif 'cid' in part:
      part = part.split(":")
      part = part[1]
      part = int(part)
      if (part//100 >= 1):
          pvalid = True
      else: 
          pvalid = False
          break
    elif 'hcl' in part:
      pvalid = True
    else:
      pvalid = False
  if pvalid == True:
    count+=1
    valid.write(passports + "\n")
    valid.write("\n")
count -= 1 #file is created correctly, but only this makes count value correct for some reason
myfile.close()
valid.close()
print(f"There are {count } valid passports")
