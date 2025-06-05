#include<iostream>
using namespace std;

bool triproduct(int n) {
    for (int i = 0; i < n; i++) {
        if ((i * (i + 1) * (i + 2)) == n) {
            return true;
        }
    }
    return false;
}

int main() {
    int n = 120;
    bool answer = triproduct(n);
    if (answer == true) {
        cout << "This is a triproduct number" << endl;
    }
    else {
        cout << "Not a triproduct number" << endl;
    }
    return 0;
}