#include <iostream>
using std::cin, std::cout, std::endl;

bool isHappy(int n)
{
    // n = 28
    while (n != 1 && n != 4)
    {
        int sum = 0;
        while (n > 0)
        {
            // get the one's digit
            int digit = n % 10;
            sum += digit * digit;
            // update n to remove the last digit
            n /= 10;
        }
        // update n to be the sum
        // sum = 8*8 + 2*2 = 68
        n = sum;
    }
    if (n == 1)
        return true;
    return false;
}

int main()
{
    cout << std::boolalpha;
    cout << "Is 4 happy? " << isHappy(4) << endl;
    cout << "Is 13 happy? " << isHappy(13) << endl;
    cout << "Is 28 happy? " << isHappy(28) << endl;
    return 0;
}
