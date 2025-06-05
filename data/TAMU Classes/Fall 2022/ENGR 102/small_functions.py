# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      576
# Assignment:   Lab 9.16
# Date:         03 November 2022

from math import*

def parta(r_sphere, r_hole):
    #input(float("Enter radius of sphere: "))
    #input(float("Enter radius of hole: "))
    r_sphere = float(r_sphere)
    r_hole = float(r_hole)
    bead = ((4/3)* pi) * ( ((r_sphere**2)-(r_hole**2)) ** (3/2))
    return(bead)
print(parta(1,.5))
    

def partb (n):
    #n = input(int("Enter any number: "))
    # go through iterations of n between 1 and 2
    for i in range (1,n,2):
        num = [i]
        for j in range(i,n,2):
            num.append(j+2)
            if sum(num) == n:
                return num
    if sum != n:
        return False
        # go through iterations of 1 in n 
        #if the sum doesnt equal the number return false
#x = partb(15)
#print(x)
                    
    # take these inputs and create a single string
    #name = input(str("Enter your name: "))
    #company = input(str('Enter company name: "))
    #email = input(str("Enter your email address: "))
def partc(character, name, company, email):
    #Finding the length of all the inputs to find out how wide the card needs to be.
 lenname = len(name)
 lencompany = len(company)
 lenemail = len(email)
 if lenname > lencompany and lenname > lenemail:
   cardlen = lenname + 6
   companylim = (lenname - lencompany) / 2
   emaillim = (lenname - lenemail) / 2
   space = ' '
   card = str(
     f'{cardlen * character}\n{character}  {name}  {character}\n{character}  '
     f'{int(companylim) * space}{company}{int(companylim) * space}  '
     f'{character}\n{character}  {int(lenemail) * space}{email}{int(lenemail) * space}  '
     f'{character}\n{cardlen * character}')
 elif lenemail > lencompany and lenemail > lenname:
   cardlen = lenemail + 6
   companylim = (lenemail - lencompany) / 2
   namelim = (lenemail - lenname) / 2
   space = ' '
   card = str(
     f'{cardlen * character}\n{character}  {int(namelim) * space}{name}{int(namelim) * space}  '
     f'{character}\n{character}  {int(companylim) * space}{company}{int(companylim) * space}  '
     f'{character}\n{character}  {email}  {character}\n{cardlen * character}')
 else:
   cardlen = lencompany + 6
   namelim = (lencompany - lenname) / 2
   emaillim = (lencompany - lenemail) / 2
   space = ' '
   card = str(
     f'{cardlen * character}\n{character}  {int(namelim) * space}{name}{int(namelim) * space}   '
     f'{character}\n{character}  {company}  {character}\n{character}  '
     f'{int(emaillim) * space}{email}{int(emaillim) * space}  {character}\n{cardlen * character}')
 return card
#partc('*', 'Dr. Ritchey', 'Texas A&M University', 'snritchey@tamu.edu')
#partc = ('♥', 'Queen of Hearts', 'Bicycle Cards', 'off@heads.net')


def partd(A):
    #sort the list first
    A.sort()
    if len(A) % 2 == 1:
        return(A[0], A[(len(A)//2)], A[len(A)-1])
    else:
        median = (A[(len(A)//2)-1] + A[len(A)//2])/2
        return(A[0], median, A[len(A)-1])
    
def parte (T, D):
    #T = input(str('Input a list of times:))
    #D = input(str('Input a list of distances))
    vel_list = []
    for i in range(len(T)-1):
        vel_list.append((D[i+1]-D[i])/(T[i+1]-T[i]))
    return vel_list
    
    
def partf (L):
    #L = input(int('Enter a length: '))
    Llen = len(L)
    for i in range(Llen):
        #Go through the input
        for j in range(Llen):
            inpt = L[i] + L[j]
            if inpt == 2026 and i != j:
                return(L[i] * L[j])
                break
    else:
        if inpt != 2026:
            return False
#b = partf([26, 125, 225, 1125, 2026, 3025, 4025, 5025, 6025, 7025, 8025, 9025, 2000])
#print(b)