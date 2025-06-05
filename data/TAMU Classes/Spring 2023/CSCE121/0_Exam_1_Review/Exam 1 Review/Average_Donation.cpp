#include <iostream>

using namespace std;

unsigned int rightShift(unsigned int num, unsigned int digits_to_shift) {
    return num >> digits_to_shift;
}

int main() {
    unsigned int num;
    unsigned int digits_to_shift;
    cin >> num;
    cin >> digits_to_shift;
    cout << rightShift(num, digits_to_shift) << endl;
    return 0;
}
