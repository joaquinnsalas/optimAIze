bool isNumericPalindrome(int n) {
    // If the number is negative, make it positive
    if (n < 0) {
        n = -n;
    }

    // Compute the reverse of the number
    int reverse = 0;
    int original = n;
    while (original > 0) {
        reverse = 10 * reverse + original % 10;
        original /= 10;
    }

    // Compare the original number with its reverse
    return (n == reverse);
}
