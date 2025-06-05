#include <iostream>
#include <sstream>
#include <fstream>
#include <cmath>
#include "functions.h"
using std::cout, std::endl, std::string, std::ifstream, std::runtime_error;

int energy(Pixel** image, int x, int y, int width, int height) { 
  int EnergyX = 0;
  int EnergyY = 0;
  int totalEnergy = 0;

  int red = 0;
  int green = 0;
  int blue = 0;

  if (x == (width-1)) {
    red = image[0][y].r - image[x-1][y].r;
    green = image[0][y].g - image[x-1][y].g;
    blue = image[0][y].b - image[x-1][y].b;
  } 
  else if(x == 0) {
    red = image[x+1][y].r - image[width-1][y].r;
    green = image[x+1][y].g - image[width-1][y].g;
    blue = image[x+1][y].b - image[width-1][y].b;
  } 
  else {
    red = image[x+1][y].r - image[x-1][y].r;
    green = image[x+1][y].g - image[x-1][y].g;
    blue = image[x+1][y].b - image[x-1][y].b;
  }
  EnergyX = pow(red, 2) + pow(green, 2) + pow(blue, 2);

  red = 0;
  green = 0;
  blue = 0;

  if (y == (height-1)) {
    red = image[x][0].r - image[x][y-1].r;
    green = image[x][0].g - image[x][y-1].g;
    blue = image[x][0].b - image[x][y-1].b;
  } else if(y == 0) {
    red = image[x][y+1].r - image[x][height-1].r;
    green = image[x][y+1].g - image[x][height-1].g;
    blue = image[x][y+1].b - image[x][height-1].b;
  } else {
    red = image[x][y+1].r - image[x][y-1].r;
    green = image[x][y+1].g - image[x][y-1].g;
    blue = image[x][y+1].b - image[x][y-1].b;
  }
  EnergyY = pow(red, 2) + pow(green, 2) + pow(blue, 2);

  totalEnergy = EnergyX + EnergyY;
  return totalEnergy;
}

unsigned int energy(Pixel image[][MAX_HEIGHT], unsigned int x, unsigned int y, unsigned int width, unsigned int height) {
    int Rx, Gx, Bx, Ry, Gy, By;

    // Calculate x-gradient
    if (x == 0) { // handle leftmost column
        Rx = abs(image[x + 1][y].r - image[width - 1][y].r);
        Gx = abs(image[x + 1][y].g - image[width - 1][y].g);
        Bx = abs(image[x + 1][y].b - image[width - 1][y].b);
    } else if (x == width - 1) { // handle rightmost column
        Rx = abs(image[0][y].r - image[x - 1][y].r);
        Gx = abs(image[0][y].g - image[x - 1][y].g);
        Bx = abs(image[0][y].b - image[x - 1][y].b);
    } else {
        Rx = abs(image[x + 1][y].r - image[x - 1][y].r);
        Gx = abs(image[x + 1][y].g - image[x - 1][y].g);
        Bx = abs(image[x + 1][y].b - image[x - 1][y].b);
    }
    int xGrad = Rx * Rx + Gx * Gx + Bx * Bx;

    // Calculate y-gradient
    if (y == 0) { // handle topmost row
        Ry = abs(image[x][y + 1].r - image[x][height - 1].r);
        Gy = abs(image[x][y + 1].g - image[x][height - 1].g);
        By = abs(image[x][y + 1].b - image[x][height - 1].b);
    } else if (y == height - 1) { // handle bottommost row
        Ry = abs(image[x][0].r - image[x][y - 1].r);
        Gy = abs(image[x][0].g - image[x][y - 1].g);
        By = abs(image[x][0].b - image[x][y - 1].b);
    } else {
        Ry = abs(image[x][y + 1].r - image[x][y - 1].r);
        Gy = abs(image[x][y + 1].g - image[x][y - 1].g);
        By = abs(image[x][y + 1].b - image[x][y - 1].b);
    }
    int yGrad = Ry * Ry + Gy * Gy + By * By;

    // Compute energy
    return xGrad + yGrad;
}

  for (unsigned int i = 0; i < height; i++) {
    for (unsigned int j = i; j < width; j++) {
      // swap image[i][j] with image[j][i]
      Pixel temp = image[i][j];
      image[i][j] = image[j][i];
      image[j][i] = temp;
    }
  }
  // update width and height
  unsigned int temp = width;
  width = height;
  height = temp;
