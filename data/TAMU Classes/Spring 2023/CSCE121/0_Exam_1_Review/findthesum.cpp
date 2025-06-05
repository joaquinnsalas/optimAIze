#include <iostream>
using namespace std;

int main() {
    const int MAX_SIZE = 5000;
    int n, k;
    int nums[MAX_SIZE];
    cin >> n;
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    cin >> k;

    bool found_pair = false;
    for (int i = 0; i < n; i++) {
        for (int j = i+1; j < n; j++) {
            if (nums[i] + nums[j] == k) {
                cout << nums[i] << " " << nums[j] << endl;
                found_pair = true;
            }
        }
    }

    if (!found_pair) {
        cout << "none" << endl;
    }

    return 0;
}
