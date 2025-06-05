#include <iostream>

using namespace std;

int findLargest(int arr[], int n) {
    int largest = arr[0]; // Set the largest element to the first element of the array
    for (int i = 1; i < n; i++) { // Loop over the array starting from the second element
        if (arr[i] > largest) { // If the current element is larger than the largest so far
            largest = arr[i]; // Update the largest element
        }
    }
    return largest; // Return the largest element
}

int main() {
    int arr[] = {1, 5, 10, 2, 8};
    int n = sizeof(arr)/sizeof(arr[0]);
    int largest = findLargest(arr, n);
    cout << "The largest element in the array is: " << largest << endl;
    return 0;
}
