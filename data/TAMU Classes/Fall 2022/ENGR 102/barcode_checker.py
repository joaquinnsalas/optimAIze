# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      576
# Assignment:   Lab 11.11 Barcode Checker
# Date:         17 November 2022

openfile = input('Enter the name of the file: ')

#first, open the file to start going through the barcodes
findfile = open(f"{openfile}", "r") #open and read
new = open('valid_barcodes.txt', 'w')


    
validbarcodes = 0
for find in findfile:
    odd = []
    even = []
    for i in range(1, 12, 2):
        even.append(find[i])
    for i in range(0, 12, 2):
        odd.append(find[i])
    fodd = 0
    feven = 0
    for i in range(len(odd)):
        fodd += int(odd[i])
    for i in range(len(even)):
        feven += int(even[i])
    feven *= 3
    fodd += feven
        
    fodd = str(fodd)
    final = fodd[-1]
    final = 10 - int(final)  
    lastbarcodedigit = int(find.strip()[-1])
        
    if lastbarcodedigit == final:
        new.write(find)
        validbarcodes += 1

print(f'There are {validbarcodes} valid barcodes')
        
        
findfile.close()
new.close()
