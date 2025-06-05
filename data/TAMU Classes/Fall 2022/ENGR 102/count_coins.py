# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      576
# Assignment:   Lab 11.12 Coin Counter
# Date:         17 November 2022

opengamefile = open('game.txt', 'r')
opencoinsfile = open('coins.txt', 'w')
readgame = opengamefile.readlines()

# check through the values and the try and excepts
coin = 0
total = 0
checkstat = True
while checkstat:
    try:
        value1, stand = readgame[coin].split(' ')[0], readgame[coin].split(' ')[1]
        if value1 == 'none':
            coin+=1
        elif value1 == 'jump':
            if stand[0] == '-':
                stand = int(stand[1:]) * -1
            else:
                stand = int(stand[1:])
            coin += stand
        elif value1 == 'coin':
            if stand[0] == '-':
                opencoinsfile.write(stand)
                stand = int(stand[1:]) * -1
            else:
                opencoinsfile.write(stand[1:])
                stand = int(stand[1:])
            total += stand
            coin+=1

    except IndexError:
        checkstat = False
        
print(f'Total coins collected: {total}')
opengamefile.close()
opencoinsfile.close()
