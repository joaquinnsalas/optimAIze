# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Yuriy Astapov
#               Areen Bhayani
#               Joaquin Salas
#               Aaditya Srinivasan
# Section:      576
# Assignment:   LAB Topic 4: Pretty Equation
# Date:         20 September 2022
from math import *

# Define inputs for coefficients A, B, and C
a = int(input('Please enter the coefficient A: '))
b = int(input('Please enter the coefficient B: '))
c = int(input('Please enter the coefficient C: '))
y = ""

# Create if statements to correctly determine a + or - sign on the console
if a < 0 and a != -1:
  y = y + f"- {abs(a)}x^2 "
elif a == -1:
  y = y + "- x^2"
elif a >= 1 and a != 1:
  y = y + f"{a}x^2"
elif a == 1:
  y = y + "x^2"

# B
if a == 0:
  if b < 0 and b != -1:
    y = y + f"{abs(b)}x"
  elif b == -1:
    y = y + "x"
  elif b >= 1 and b != 1:
    y = y + f"{b}x"
  elif b == 1:
    y = y + "x"
if a != 0:
  if b < 0 and b != -1:
      y = y + f" - {abs(b)}x"
  elif b == -1:
      y = y + " - x"
  elif b >= 1 and b != 1:
      y = y + f" + {b}x"
  elif b == 1:
      y = y + " + x"
# C


if c < 0 and c != -1:
  y = y + f" - {abs(c)}"
elif c == -1:
  y = y + " - 1"
elif c >= 1 and c != 1:
  y = y + f" + {c}"
elif c == 1:
  y = y + f" + {c}" 

y = y + " = 0"

print(f'The quadratic equation is {y}')