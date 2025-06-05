#include<iostream>

using namespace std;

void rotateLeft(int**& ary, unsigned int& numRows, unsigned int& numCols) {

    //first initialize a new 2D array
    int* newarray = new int[numCols];
    for (int i = 0; i < numRows; i++) {
        newarray* = ary[i];
    }
    //Step 2: move the data into the array
    for (int i = 0; i < numCols; i++) {
        for (int j = 0; i < numRows; j++) {
            newarray[i][j];
        }
    }
    //Step 3: erase the old one
    for (int i = 0; i < numRows; i++) {
        delete[] ary;
    }
    delete[] ary;
    //Step 4: Set old eqal to new
    ary = newarray;
}

int main() {

    //Initialize the first array and populate it 
    
    if (ary == nullptr) {
        return nullptr;
    }
    if ((numRows == 0) || (numCols == 0)) {
        return nullptr;
    }
}