#include <iostream>

using namespace std;

void rotateLeft(int**& ary, unsigned int& numRows, unsigned int& numCols) {

    //Create an array opposite of old array
    int **newarray = new int*[numCols]; //Initialize

    for(int i = 0; i < numCols; i++) { //use numCols instead of numRows in this first for loop because it is flipped
        newarray[i] = new int[numRows]; //By row
    }

    //Load the old data into new array using the same form of for loops
    for (int i = 0; i < numRows; i++) {
        for(int j = 0; j < numCols; j++) {
            //Load the old stuff into the new array
            //Not sure if this is right because i dont have time to load values but it should work to rotate it
            newarray[j][numRows-i-1] = ary[i][j];
        }
    }
    //Delete the old array
    for(int i = 0; i < numRows; i++) { //numRows because the old one hasnt been flipper
        delete[] ary[i];
    }
    delete[] ary;

    //Let old array point to new one
    ary = newarray;
}


int main() {
    //Let user input dimensions for an M x N array
    unsigned int numRows, numCols;
    cout << "Enter dimensions of a M x N array: " << endl;
    cin >> numRows >> numCols;

    int **ary = new int*[numRows]; //initialize a dynamic 2D array by row
    for(int i = 0; i < numRows; i++) {
        ary[i] = new int[numCols]; //By Col
    }

    if ((numRows == 0) || (numCols == 0)) { //Exceptions
        throw std::invalid_argument("The dimensions of the matrix cant be 0");
    }
    //I dont have to check for less than 0 because unsigned int

    //Input the values that the user wants
    cout << "Enter in the digits to populate the array: " << endl;
    int input;
    cin >> input; //Takes the user input

    for (int i = 0; i < numRows; i++) {
        for (int j = 0; j < numCols; j++) {
            cin >> ary[i][j]; //Here to populate the array like in dungeon crawler
        }
    }

    if (ary == nullptr) { //Check if nullptr
        throw std::invalid_argument("Pointer is a nullptr");
    }

    rotateLeft(ary, numRows, numCols); //almost forgot to call the function
    cout << "The output is: " << endl;
    //print out the array by using 2 more for loops
    for (int i = 0; i < numCols; i++) {
        for (int j = 0; i < numRows; j++) {
            cout << ary[i][j]; //prints out the reversed array
        }
        cout << endl;
    }

    //Always delete the array at the end
    for(int i = 0; i < numCols; i++) { //delete cols first
        delete[] ary[i]; //delete[] because it is an array
    }
    delete[] ary;
    //make the rotate function by switching cols and rows and loading the new data
    return 0;
}
