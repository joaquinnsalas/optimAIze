#include <iostream>
#include <cmath>
#include "./nth_root.h"

int main() {
    {   // MINIMUM REQUIREMENT (for this lab)
        // just call the function with various values of n and x
        try {
            nth_root(0, 1); //n = 0
            nth_root(4, -1); //For B
            nth_root(-3, 0); //For C
            nth_root(1, 5); //For D
            nth_root(-1, 5); //For E
            nth_root(-4, 5); //For F
            nth_root(-10, 6); //For G
            nth_root(-3, 5); //For H
            nth_root(8, 6); //For I
            nth_root(3, 6); //For J
            nth_root(4, 0); //For K
            nth_root(3, 1); //For L
            nth_root(3, -3); //For M
            nth_root(4, 60); //For N
            nth_root(2, 1.5); //For O
        }
        catch (...) {

        }
        try {
            nth_root(0 , 2);
        }
        catch (...) {

        }
        try {
            nth_root(2 , -2);
        }
        catch (...) {

        }
        try {
            nth_root(-2, 0);
        }
        catch (...) {
            
        }
    }


    {   // TRY HARD
        // report the value
        double actual = nth_root(2, 1);
        std::cout << "nth_root(2, 1) = " << actual << std::endl;
    }

    {   // TRY HARDER
        // compare the actual value to the expected value
        double actual = nth_root(2, 1);
        double expected = 1;
        if (std::fabs(actual - expected) > 0.00005) {
            std::cout << "[FAIL] (n=2, x=1)" << std::endl;
            std::cout << "  expected nth_root(2, 1) to be " << expected << std::endl;
            std::cout << "  got " << actual << std::endl;
        } else {
            std::cout << "[PASS] (n=2, x=1)" << std::endl;
        }
    }
    return 0;
}
