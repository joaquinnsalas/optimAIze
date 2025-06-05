#include <iostream>
#include "functions.h"

using std::cout, std::endl;

bool is_valid_range(int a, int b) {
	// TODO(student): validate input range

	if ((a <= 9) && (b > 10000) && (a >= b)) {
		return false;
	}
	else if ((10 <= a) && (a <= b) && (b < 10000)) {
		return true;
	}
	/*This function returns the boolean value true if and only if inputs a and b satisfy the constraint that 10 <= a <= b < 10000.*/ 
	return false;
}


char classify_mv_range_type(int number) {
	bool ismountain = false, isvalley = false, neither = false;
    int firstdigit, seconddigit, divide = 1, numdigits;
    int divisor = number;
	numdigits = 0;
    while (divisor > 0) { //Counts the number of digits in the "number"
        numdigits++;
        divisor = divisor / 10;
    }

    for (int i = 0; i < numdigits - 1; i++) { //this will find out what to divide by
    	divide *= 10;						  // Ex. 12345 / 10 ^ (numdigits - 1)
	}

	for (int j = 1; j < numdigits; j++) { 

		firstdigit = number / divide;	// To grab the first digit in the number
		number = number % divide;		// This saves number as the remainder from the first operation
		divide = (divide / 10);			// Divide divisor by 10 to lower what next number will be divided by
		seconddigit = number / divide;  // Saves second number

		if ((j % 2) != 0) { //While in odd iteration, ex d1 && d2 or d3 && d4

			if (firstdigit > seconddigit) {
				isvalley = true;
			}
			else if (firstdigit < seconddigit) {
				ismountain = true;
			}
			else {
				neither = true;
			}
		}
		else if ((j % 2) == 0) { //While in even iteration, ex d2 && d3.

			if (firstdigit < seconddigit) {
				isvalley = true;
			}
			else if (firstdigit > seconddigit) {
				ismountain = true;
			}
			else {
				neither = true;
			}
		}
	}
	if ((ismountain == true) && (isvalley == false) && (neither == false)) {
		return 'M';
	}
	else if ((ismountain == false) && (isvalley == true) && (neither == false)) {
		return 'V';
	}
	else {
		return 'N';
	}
}
void count_valid_mv_numbers(int a, int b) {
	// TODO(student): count the number of valid mountain ranges and valley
	// ranges in the range [a, b] and print out to console using the format
	// in Requirement 4 of the homework prompt
	int countM = 0, countV = 0, i = 0;
	for (i = a; i < b + 1; ++i) {

		if (classify_mv_range_type(i) == 'M') {
			countM++;
		}
		else if (classify_mv_range_type(i) == 'V') {
			countV++;
		}
	}
	cout << "There are " << countM << " mountain ranges and " << countV << " valley ranges between " << a << " and " << b << "." << endl;
}