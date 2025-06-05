"""
Created on Thu Oct 13 08:04:24 2022
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
# Assignment:   LAB Topic 7: go_moves
# Date:         23 October 2022

#create 9 by 9 board
game_list = []
for i in range(1,10):          #create list of lists filled with periods
     temp = []                 #period indicates no value
     for j  in range(1,10):
         temp.append('.')
     game_list.append(temp)
error =''
turn = 1
cont = input('Do you want to Stop? ("Yes"/"No") ')
while cont != "Yes":
  x = int(input('what x value do you want? '))          #ask for x and y coordinates
  y = int(input('what y value do you want? '))
  if turn % 2 == 1 and x <= 9 and y <= 9 and x>=1 and y >=1:    #check whose turn it is and whether x and y coordinates are in bounds
    if game_list[y-1][x-1] == '.':                              #check if there is already a value on x and y coordinate
      game_list[y-1][x-1] = 'o'
      print('Player 1 Moved!')
    else:                             #if there is a value, send error message and prompt whether to continue game or not
      error = input('Error: There is a stone in this spot; "again" or "Stop" ')
      if error == 'Stop':
        break
      elif error == 'again':
        turn = turn - 1
  elif turn % 2 == 0 and x <= 9 and y <= 9 and x>= 1 and y >=1:  #check whose turn it is and whether x and y coordinates are in bounds
    if game_list[y-1][x-1] == '.':    #check if there is already a value on x and y coordinate
      game_list[y-1][x-1] = '*'
      print('Player 2 Moved!')
    else:                             #if there is a value, send error message and prompt whether to continue game or not
      error = input('Error: There is a stone in this spot; "again" or "Stop" ')
      if error == 'Stop':
        break
      elif error == 'again':
        turn = turn - 1
  else:                                #if x and y coordinates not in bounds, error message sent and prompt to continue game
    error = input('Error: The stone is off the board; "again" or "Stop" ')
    if error == 'Stop':
      break
    elif error == 'again':
      turn = turn - 1
  #traversing the loop 
  for p in game_list:                  #print game grid after each move and error
    for i in p:
      print(i, end = " ")
    print()
  cont = input('Do you want to Stop? ("Yes"/"No") ')
  turn +=1             #changes players' turns

