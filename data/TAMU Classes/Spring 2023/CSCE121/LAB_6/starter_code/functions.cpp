#include <iostream>
#include "functions.h"
using namespace std;

void function_one(int i, int& j) {
    i += 2;
    j += 1;
	// TODO: implement function_one so that it takes two integer arguments i and j, adds 2 to i,
    // adds 1 to j, (after execution of the function, only j is changed)
}

void function_two(example& foo) {
    foo.value += 1;
    // TODO: implement function_two so that it takes an argument of type example, and increments
    // its integer by 1 (should persist after the function)
}

void function_three(int* k, int& l) {
    l += 1;
    *k += 1;
    // TODO: implement function_three so that it increments both variables by one (both changes must
    // persist after the function call)
}

void function_four(int bar[], int size, int& lowest, int& highest) {
    for (int i = 0; i < size; i++) {
        bar[i] += 2;
    }
    lowest = bar[0];
    highest = bar[0];
    for (int j = 1; j < size; j++) {
        if (bar[j] < lowest) {
            lowest = bar[j];
        }
        if (bar[j] > highest) {
            highest = bar[j];
        }
    }
    // TODO: implement function_four so that it increments every value by two and then sets lowest /
    // highest to the min / max of the array (all changes must persist after the function call)
}