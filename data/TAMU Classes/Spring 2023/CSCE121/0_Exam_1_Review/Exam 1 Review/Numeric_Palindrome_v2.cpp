// This program determines whehter an integer is a numeric palindrome.
// It does not use an array.

#include <iostream>
using std::cout, std::endl, std::boolalpha;

bool isNumericPalindrome(int n)
{
    if (n == 0)
        return true;
    if (n < 0)
        n = n * (-1);   // convert n into a positive number

    int reverse = 0;
    int tmp = n;

    // do the number slicing from right to left
    // suppose tmp = 123
    // reverse = 0 * 10 + 3  = 3 in the first iteration
    // in the second iteration, reverse = 3 * 10 + 2 = 32
    // in the third iteration, reverse = 32 * 10 + 1 = 321
    while (tmp > 0)
    {
        reverse = reverse * 10 + tmp % 10;
        tmp /= 10;
    }

    cout << "reverse: " << reverse << endl;
    // if n is a numeric palindrome, then reverse = n
    if (reverse != n)
        return false;

    return true;
}

int main()
{
    // testing the funciton isNumericPalindrome
    cout << boolalpha;
    cout << "121: " << isNumericPalindrome(121) << endl;
    cout << "-121: " << isNumericPalindrome(-121) << endl;
    cout << "220: " << isNumericPalindrome(220) << endl;
    cout << "-220: " << isNumericPalindrome(-220) << endl;
    cout << "1834381: " << isNumericPalindrome(18344381) << endl;
    cout << "-1834381: " << isNumericPalindrome(-18344381) << endl;
    cout << "12345: " << isNumericPalindrome(12345) << endl;
    cout << "1: " << isNumericPalindrome(1) << endl;
    cout << "0: " << isNumericPalindrome(0) << endl;

    return 0;
}
