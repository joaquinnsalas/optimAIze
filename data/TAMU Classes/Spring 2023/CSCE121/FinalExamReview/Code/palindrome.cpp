// see if an input number is a numeric palindrome.
#include<iostream>
using std::cin, std::cout, std::endl;

/* 
 * if num is a palindrome, after removing its first digit and last digit, it is
 * still a palindrome, e.g., 12321
 * 232
 */

/*
 * if num is not a palindrome, either:
 * (1) the first digit and the last digit are not equal, e.g., 234
 * (2) the first digit and the last digit is equal. The resulting value after
 * removing the first digit and the last digit is not a palindrome, e.g., 1451
 * 45
 */

bool isPalindrome(int num)
{
   int num_digits = 0;
   int multiplier = 1;
   int newValue = 0;
   
   // compute last digit
   int last_digit = num % 10;
   
   // a single digit is a palindrome
   // base case
   if (last_digit == num) {
      return true;
   }
   
   // compute first digit
   int first_digit = num;
   do {
      first_digit /= 10;
      ++num_digits;
      multiplier *= 10;
   } while (first_digit > 9);
   
   // if first and last digits are equal, check if the newValue is a palindrome
   // newValue is a palindrome if and only if num is a palindrome  
   // e.g., num = 42324, first_digit = 4, last_digit = 4, nultiplier = 10000
   // newValue = (42324 - 4*10000 - 4) / 10 = 232
   if (first_digit == last_digit) {
      newValue = (num - first_digit*multiplier - last_digit)/10;
      return isPalindrome(newValue);
   }
   // if first and last digits are not equal it is not a palindrome
   return false;
} 

int main()
{
   int num;
   cout << "Enter an integer (max 19 digits) -> ";
   cin >> num;
   if (isPalindrome(num))
      cout << num << " is a palendrome." << endl;
   else
      cout << num << " is not a palindrome." << endl;

   return 0;
}

