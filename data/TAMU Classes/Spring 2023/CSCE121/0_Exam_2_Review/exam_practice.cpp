/*
Notes on Resizing an array
*/
#include <iostream>

using namespace std;

void Create2dArray(int**& ary, unsigned int& numRows, unsigned int& numCols) {

    //Step 1: Create an array opposite of old array
    int **newarray = new int*[numCols]; //Initialize

    for(int i = 0; i < numCols; i++) { //use numCols instead of numRows in this first for loop because it is flipped
        newarray[i] = new int[numRows];
    }

    //Load the old data into new array using the same form of for loops
    for (int i = 0; i < numRows; i++) {
        for(int j = 0; j < numCols; j++) {
            //Load the old stuff into the new array
            newarray[j][numRows-i-1] = [i][j];
        }
    }
    //Delete old array
    for(int i = 0; i < numRows; i++) { //numRows because the old one hasnt been flipper
        delete[] ary[i];
    }
    delete[] ary;

    //Let old array point to new one
    ary = newarray;
}


int main() {

    //Let user input dimensions for an M x N array
    int numRows, numCols;
    cout << "Enter dimensions of a M x N array: " << endl;
    cin >> numRows >> numCols;

    int **ary = new int*[numRows]; //initialize a dynamic 2D array by row
    for(int i = 0; i < numRows; i++) {
        ary[i] = new int[numCols]; //By Col
    }

    if ((numRows == 0) || (numCols == 0)) { //Exceptions
        std::throw(invalid_argument("Cant be 0"));
    }
    //I dont have to check for less than 0 because unsigned int

    //Input the values that the user wants
    cout << "Enter in any digits to populate array: " << endl; 
    int i , j;
    for (i = 0; i < numRows; i++) {
        for (j = 0; j < numCols; j++) {
            cin >> ary[i][j];
        }
    }

    if (ary == nullptr) {
        std::throw(invalid_argument("Nullptr"));
    }

    //Always delete the array
    for(int i = 0; i < numCols; i++) {
        delete[] ary[i];
    }
    delete[] ary;

    return 0;
}
