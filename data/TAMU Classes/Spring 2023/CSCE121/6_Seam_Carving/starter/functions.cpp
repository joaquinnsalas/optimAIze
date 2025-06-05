#include <iostream>
#include <sstream>
#include <fstream>
#include <cmath>
#include "functions.h"

using std::cout, std::endl, std::string, std::ifstream, std::ios;

void initializeImage(Pixel image[][MAX_HEIGHT]) {
  // iterate through columns
  for (unsigned int col = 0; col < MAX_WIDTH; col++) {
    // iterate through rows
    for (unsigned int row = 0; row < MAX_HEIGHT; row++) {
      // initialize pixel
      image[col][row] = {0, 0, 0};
    }
  }
}

void loadImage(string filename, Pixel image[][MAX_HEIGHT], unsigned int& width, unsigned int& height) {
  // TODO: implement (part 1)
  ifstream myfile (filename); //ifstream to read from files
  if (!myfile.is_open()) { // check if the file was unsuccessfully opened
    throw std::runtime_error("Failed to open " + filename);
  }
  string filetype;
  myfile >> filetype; //Make sure it is a RGB color image in ASCII in the first line
  if ((filetype != "P3") && (filetype != "p3")) { //Check if file type is "P3" or "p3"
    throw std::runtime_error("Invalid type " + filetype);
  }
  //Check second line to grab dimensions
  myfile >> width >> height; //is the width and height of the image in pixels
  if (((width <= 0) || (height <= 0)) || ((width > MAX_WIDTH) || (height > MAX_HEIGHT))) { //Both dimensions should be positive integers and less than the maximum’s 
    throw std::runtime_error("Invalid dimensions");
  }
  unsigned int maxcolor; //initialize the max value for each color (third line)
  myfile >> maxcolor; //gets the third line
  if (maxcolor != 255) {
    throw std::runtime_error("Invalid color value");
  }

  int r, g, b;
  string a = "";
  for (unsigned int row = 0; row < height; row++) {
    for (unsigned int col = 0; col < width; col++) {
      myfile >> r;
      if (myfile.fail()) {
        throw std::runtime_error("Invalid color value");
      }
      myfile >> g;
      if (myfile.fail()) {
        throw std::runtime_error("Invalid color value");
      }
      myfile >> b;
      if (myfile.fail()) {
        throw std::runtime_error("Invalid color value");
      }
      if (((r < 0) || (r > 255)) || ((g < 0) || (g > 255)) || ((b < 0) || (b > 255))) { //If there is an invalid pixel value
        throw std::runtime_error("Invalid color value");
      }
      image[col][row].r = r;
      image[col][row].g = g;
      image[col][row].b = b;
    }
  }
  myfile >> a;
  if (a != "") {
    throw std::runtime_error("Too many values");
  }
}

void outputImage(string filename, Pixel image[][MAX_HEIGHT], unsigned int width, unsigned int height) {
  // TODO: implement (part 1)
  std::ofstream myfile(filename);
  if (!myfile.is_open()) { // check if the file was unsuccessfully opened
    throw std::runtime_error("Failed to open " + filename);
  }
  string filetype = "P3";
  myfile << filetype << "\n";
  myfile << width << " " << height << "\n";
  unsigned int maxcolor = 255; //initialize the max value for each color (third line)
  myfile << maxcolor << "\n";
  for (unsigned int row = 0; row < height; row++) { //first for loop to iterate rows
    for (unsigned int col = 0; col < width; col++) {
      myfile << image[col][row].r << "\n";
      myfile << image[col][row].g << "\n";
      myfile << image[col][row].b << "\n";
    }
  }
}

unsigned int energy(Pixel image[][MAX_HEIGHT], unsigned int x, unsigned int y, unsigned int width, unsigned int height) {
  // TODO: implement (part 1)
  int leftmost = 0; 
  if (x == 0) {
    leftmost = (width - 1);
  } else {
    leftmost = x - 1;
  }
  int rightmost = 0; 
  if (x == (width - 1)) {
    rightmost = 0;
  } else {
    rightmost = x + 1;
  }
  int topmost = 0; 
  if (y == 0) {
    topmost = height - 1;
  } else {
    topmost = y - 1;
  }
  int bottommost = 0;
  if (y == (height - 1)) {
    bottommost = 0;
  } else {
    bottommost = y + 1;
  }
  int rxchange = 0, gxchange = 0, bxchange = 0;
  int rychange = 0, gychange = 0, bychange = 0;
  int Gx = 0, Gy = 0;
  int energy = 0;

  rxchange = abs(image[rightmost][y].r - image[leftmost][y].r);
  gxchange = abs(image[rightmost][y].g - image[leftmost][y].g);
  bxchange = abs(image[rightmost][y].b - image[leftmost][y].b);

  rychange = abs(image[x][bottommost].r - image[x][topmost].r);
  gychange = abs(image[x][bottommost].g - image[x][topmost].g);
  bychange = abs(image[x][bottommost].b - image[x][topmost].b);

  Gx = pow(rxchange, 2) + pow(gxchange, 2) + pow(bxchange, 2);
  Gy = pow(rychange, 2) + pow(gychange, 2) + pow(bychange, 2);

  energy = Gx + Gy;

  return energy;
}

// uncomment functions as you implement them (part 2)

unsigned int loadVerticalSeam(Pixel image[][MAX_HEIGHT], unsigned int start_col, unsigned int width, unsigned int height, unsigned int seam[]) {
  // TODO: implement (part 2)
  int down = 0, left = 0, right = 0, verticalSeamEnergy = 0;
  verticalSeamEnergy = energy(image, start_col, 0, width, height); //Find energy of first pixel
  seam[0] = start_col; //Set the first item in the seam to whatever start_col is brought in
  for (unsigned int row = 1; row < height; row++) { //iterate through each vertical row starting after 0
    down = start_col;
    if ((start_col + 1) <= width) { //makes sure not out of bounds
    left = start_col + 1;
    } else {
      left = start_col;
    }
    if (start_col == 0) {
      right = 0;
    } else {
      right = start_col - 1;
    }
    //find energys for all paths after determining edges
    int pathdown = energy(image, down, row, width, height);
    int pathleft = energy(image, left, row, width, height);
    int pathright = energy(image, right, row, width, height);
    //Chose the greatest number considering bounds
    if ((pathdown <= pathleft) && (pathdown <= pathright)) {
      verticalSeamEnergy += pathdown;
      seam[row] = down;
    } else if ((pathleft <= pathdown) && (pathleft <= pathright)) {
      verticalSeamEnergy += pathleft;
      seam[row] = left;
    } else if ((pathright < pathdown) && (pathright < pathleft)) {
      verticalSeamEnergy += pathright;
      seam[row] = right;
    } else { //Else to make sure every possible combination is caught
      cout << "Something here is wrong" << endl;
    }
    start_col = seam[row]; //Load the seam table with the seam chosen
  }
  return verticalSeamEnergy; //totalenergy of seam
}

unsigned int loadHorizontalSeam(Pixel image[][MAX_HEIGHT], unsigned int start_row, unsigned int width, unsigned int height, unsigned int seam[]) {
  // TODO: implement (part 2)
  int forward = 0, left = 0, right = 0, horizontalSeamEnergy = 0;
  horizontalSeamEnergy = energy(image, 0, start_row, width, height);
  seam[0] = start_row;
  for (unsigned int col = 1; col < width; col++) {
    forward = start_row;
    if (start_row == 0) {
      left = 0;
    } else {
      left = start_row - 1;
    }
    if ((start_row + 1) <= height) {
      right = start_row + 1;
    } else {
      right = start_row;
    }
    int pathforward = energy(image, col, forward, width, height);
    int pathleft = energy(image, col, left, width, height);
    int pathright = energy(image, col, right, width, height);

    if ((pathforward <= pathleft) && (pathforward <= pathright)) {
      horizontalSeamEnergy += pathforward;
      seam[col] = forward;
    } else if ((pathleft <= pathforward) && (pathleft <= pathright)) {
      horizontalSeamEnergy += pathleft;
      seam[col] = left;
    } else if ((pathright < pathforward) && (pathright < pathleft)) {
      horizontalSeamEnergy += pathright;
      seam[col] = right;
    } else {
      cout << "Something is wrong here" << endl;
    }
    start_row = seam[col];
  }
  return horizontalSeamEnergy;
}

void findMinVerticalSeam(Pixel image[][MAX_HEIGHT], unsigned int width, unsigned int height, unsigned int seam[]) {
  // TODO: implement (part 2)
  unsigned int leastEnergy = 0;
  unsigned int minEnergy = loadVerticalSeam(image, 0, width, height, seam); //compare verticalSeamEnergy

  for (unsigned int col = 0; col < width; col++) {
    if (minEnergy >= loadVerticalSeam(image, col, width, height, seam)) {
      leastEnergy = col;
      minEnergy = loadVerticalSeam(image, col, width, height, seam);
    }
  }
  loadVerticalSeam(image, leastEnergy, width, height, seam);
}

void findMinHorizontalSeam(Pixel image[][MAX_HEIGHT], unsigned int width, unsigned int height, unsigned int seam[]) {
  // TODO: implement (part 2)
  unsigned int leastEnergy = 0;
  unsigned int minEnergy = loadHorizontalSeam(image, 0, width, height, seam);

  for (unsigned int row = 0; row < height; row++) {
    if (minEnergy >= loadHorizontalSeam(image, row, width, height, seam)) {
      leastEnergy = row;
      minEnergy = loadHorizontalSeam(image, row, width, height, seam);
    }
  }
  loadHorizontalSeam(image, leastEnergy, width, height, seam);
}

void removeVerticalSeam(Pixel image[][MAX_HEIGHT], unsigned int& width, unsigned int height, unsigned int verticalSeam[]) {
  // TODO: implement (part 2)
  for (unsigned int row = 0; row < height; row++) {
    for (unsigned int column = verticalSeam[row]; column < (width - 1); column++) {
      image[column][row] = image[column + 1][row];
    }
  }
  width -= 1;
}

void removeHorizontalSeam(Pixel image[][MAX_HEIGHT], unsigned int width, unsigned int& height, unsigned int horizontalSeam[]) {
  // TODO: implement (part 2)
  for (unsigned int col = 0; col < width; col++) {
    for (unsigned int row = horizontalSeam[col]; row < (height - 1); row++) {
      image[col][row] = image[col][row + 1];
    }
  }
  height -= 1;
}
