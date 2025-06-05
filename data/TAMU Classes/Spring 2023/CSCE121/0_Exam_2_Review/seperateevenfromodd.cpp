#include <iostream>
using namespace std;

/*
Separate even from odds
Write a function that receives an array A of n integers (all elements >= 0) and returns a 
dynamically allocated array containing all even elements of A first, then all odd elements
of A. The signature of the function is:

*/

int* separate_even_odd(int* A, unsigned int n) {

    //Count number of evens to know how big to make the array
    int even;
    int odd;
    for (int i = 0; i < n; i++) {
        if ((i % 2) == 0) {
            even++;
        }
    }
}


int main() {

    int* A = nullptr;
    unsigned int n;
    int numbers;
    cout << "How many numbers are you entering: " << endl;
    cin >> n;
    cout << "Enter numbers: " << endl;
    cin >> numbers;
    //Creates a 1D array of integers
    A = new int[n];
    for (int i = 0; i < n; i++) {
        cin >> n
    }
}