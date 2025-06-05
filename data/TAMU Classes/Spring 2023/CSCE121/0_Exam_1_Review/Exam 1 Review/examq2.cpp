#include<iostream>

using namespace std;

int getSum(int ary[], int size, int start_index) {
    cin >> size;
    int ary[size];
    cin >> start_index;
    int error;
    
    int runningSum;
    //First check if the start index is in range and return 100
    if (start_index >= size) {
        return 100;
    }
    for (int i = 0; i < size; i++) { //Starts at the rightmost of the list
        if ((ary[-1] % 2) != 0) { // If the rightmost digit is odd
            ary[i] -= ary[-1]; //subtract from current index to get next index
            runningSum += ary[i]; //Keep running sum
            if (start_index >= size) { //If out of range
                error = runningSum + 100; //Add 100
                return error; //Return that number
            }
        }
        if ((ary[-1] % 2) == 0) { //If even
            ary[i] += ary[-1];  //add to current index to get next index
            runningSum += ary[i]; //Keep running sum 
            if (start_index >= size) {
                error = runningSum + 100;
                return error;
            }
        }
        if (ary[-1] == ary[0]) {
            runningSum += ary[i];
            return runningSum;
        }
    }
    //If even, add to current index to get next index
    //if equal, return the running sum
    //If next index is outside array bounds
    //Add 100 
    //reuturn running sum

}