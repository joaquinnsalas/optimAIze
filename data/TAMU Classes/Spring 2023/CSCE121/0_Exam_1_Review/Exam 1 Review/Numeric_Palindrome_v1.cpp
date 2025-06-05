// This program determines whehter a positive number is Numeric Palindrome.
// It uses an array to do it.

#include <iostream>
using std::cout, std::endl, std::boolalpha;

bool isNumericPalindrome(int n)
{
    if (n == 0)   // 0 is a numeric palindrome
        return true;
    if (n < 0)
        n = n * (-1);   // convert n into a positive number

    // initialize the array
    int digits[100] = {};   // used to store digits
    
    // i keeps track of the index of digits[100] to fill
    int i = 0, size = 0;

    //extract the digits of n, the digits are stored in the array
    while (n > 0)
    {
        // get the last digit (one's digit)
        digits[i] = n % 10;
        i ++; 
        size ++;
        n /= 10;
    }

    // if n is a numeric palindrome, then digits[i] == digits[size-1-i]
    // for every i = 0, 1, ..., size-1
    for (i = 0; i < size; i++)
    {
        if (digits[i] != digits[size - 1 - i])
            return false;
    }
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
