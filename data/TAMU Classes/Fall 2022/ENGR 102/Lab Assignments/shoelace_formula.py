# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Yuriy Astapov
#               Areen Bhayani
#               Joaquin Salas
#               Aaditya Srinivasan
# Section:      576
# Assignment:   LAB Topic 9: shoelace_formula
# Date:         27 October 2022

#getpoints function
def getpoints(str):
  vert = str.split()
  lis = []
  for i in range(0,len(vert)):
    y = vert[i].split(",")
    lis.append(y)
  for i in range(0,len(lis)):
    for j in range(0,len(lis[i])):
      lis[i][j] = int(lis[i][j])
  return lis
#gets cross prod function
def cross(p1,p2):
  prod = p1[0]*p2[1] - p1[1]*p2[0]
  return prod
def shoelace(points):
  area = 0
  for i in range(0, len(points)):
    if i != len(points)-1:
      area += cross(points[i],points[i+1])
    else:
      area += cross(points[i],points[0])
  return float(area/2)

def main():
  inp = input('Please enter the vertices: ')
  print(f"The area of the polygon is {shoelace(getpoints(inp)):.1f}")
if __name__ == '__main__': 
  main()