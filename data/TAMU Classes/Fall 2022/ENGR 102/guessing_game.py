# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Joaquin Salas
# Section:      576
# Assignment:   Lab 10.14
# Date:         10 November 2022


def instructions():
    print("Guess the secret number! Hint: it's an integer between 1 and 100...")

def checking():
    
    attempts = 0
    guess = 0
    mynumber = 26
    instructions()
    guess = input('What is your guess? ')
    while (guess != mynumber):

        try:
            guess = str(guess)
            guess = int(guess)
            if int(guess) < mynumber:
                print('Too low!')
                guess = input('What is your guess? ')
                attempts += 1
            elif int(guess) > mynumber:
                print('Too high!')
                guess = input('What is your guess? ')
                attempts += 1
            elif int(guess) == mynumber:
                attempts += 1
                print(f'You guessed it! It took you {attempts} guesses.')
#except to get all the numbers that are floats or strings
        except ValueError:
            guess = input('Bad input! Try again: ')


checking()
            




                
            
    