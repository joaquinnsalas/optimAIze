#include <iostream>
#include <string>
#include <sstream>
#include "./string_calculator.h"

using namespace std;
using std::cout, std::endl;
using std::string;
using std::invalid_argument;

unsigned int digit_to_decimal(char digit) {
    // TODO(student): implement
    if ((digit >= '0') && (digit <= '9')) {
        stringstream ss;
        int decimal;
        ss << digit;
        ss >> decimal;
    //cout << digit << endl;
    return decimal;
    }
    else {
        //cout << "This number is causing error: " << digit << endl;
        throw std::invalid_argument("Not a single digit character representing a decimal.");
    }
}

char decimal_to_digit(unsigned int decimal) {
    // TODO(student): implement
    if (decimal <= 9) {
        stringstream ss;
        char digit;
        ss << decimal;
        ss >> digit;

    return digit;
    }
    else {
        throw std::invalid_argument("Not a single digit decimal.");
    }
}

string trim_leading_zeros(string num) {
    // TODO(student): implement
    int i = 0;
    bool isnegative = false;
    if (num[0] == '-') { //Check if input is negative
        i = 1;
        isnegative = true;
    }
    if (num[0] == '-') { //Remove the negative sign, Ill add it back later
        num = num.substr(1, num.length() - 1);
    }

    int numLength = num.length();
    int startnum = 0;
    for (i = 0; i < numLength; i++) { //Find the first non zero digit
        if (num[i] != '0') {
            startnum = i; //Thats where the number starts
            break;
        }
    }
    if (num.find_first_not_of('0') == string::npos) { // If all digits are 0, return an empty string
        return "0";
    }
    num = num.substr(startnum); //Remove the leading zeros
    if (isnegative) {
        num.insert(0, "-"); //Add back the negative sign
    }
    return num;
}

string add(string lhs, string rhs) {

    // TODO(student): implement
    int new_length, max_length, answer, sum; //Holds the length of the answer
    int carry = 0; //initialize carry to 0
    string finalAnswer, backwardsAnswer; //Holds the answer after being reversed

    //REMOVING SPACES
    string lhs_nospaces;
    for (char c : lhs) {
        if (!std::isspace(c)) {
            lhs_nospaces += c;
        }
    }
    lhs = lhs_nospaces;

    string rhs_nospaces;
    for (char c : rhs) {
        if (!std::isspace(c)) {
            rhs_nospaces += c;
        }
    }
    rhs = rhs_nospaces;

    bool isnegative = false;
    if ((lhs.find('-') != std::string::npos) && (rhs.find('-') != std::string::npos)) { //Check if negative
        isnegative = true;
        if (lhs[0] == '-') { //Remove the negative add it back later
            lhs = lhs.substr(1, lhs.length() - 1);
        }
        if (rhs[0] == '-') {
            rhs = rhs.substr(1, rhs.length() - 1);
        }
    }

    int len_lhs = lhs.length(); //Find length of first string
    int len_rhs = rhs.length(); //Find length of second string

    //Determine max length of the 2 strings
    if (len_lhs > len_rhs) {
        max_length = len_lhs;
    }
    if (len_rhs > len_lhs) {
        max_length = len_rhs;
    }
    if (len_lhs == len_rhs) {
        max_length = len_lhs;
    }
    
    lhs = string(max_length - len_lhs, '0') + lhs; //Add 0s so list isnt out of range
    rhs = string(max_length - len_rhs, '0') + rhs; //Add 0s so list isnt out of range

    for (int i = max_length - 1; i >= 0; i--) {

        sum = (digit_to_decimal(lhs[i]) + digit_to_decimal(rhs[i]) + carry);
        if (sum > 9) {
            carry = sum / 10;
            answer = sum % 10;
        }
        else {
            carry = 0;
            answer = sum;
        }
        backwardsAnswer += decimal_to_digit(answer);
    }
    if (carry != 0) { //If carry remains after the loop, add it as an additional digit to the end of the string
        backwardsAnswer += decimal_to_digit(carry);
    }
    new_length = backwardsAnswer.length();
    for (int i = 0; i < new_length / 2; i++) { //Reverse the order of the string to get the correct order of digits
        swap(backwardsAnswer[i], backwardsAnswer[new_length - i -1]);
    }

    if (isnegative == true) { //If both numbers are negative, add '-'
        finalAnswer = '-' + trim_leading_zeros(backwardsAnswer);
    }
    else {
        finalAnswer = trim_leading_zeros(backwardsAnswer);
    }
    return finalAnswer;
}

string multiply(string lhs, string rhs) {
    // TODO(student): implement
    string top_num, bottom_num, backwardsAnswer, total, final_answer;
    int len_bottom, len_top, multiply, answer, max_length;
    int carry = 0;

    //REMOVING SPACES
    string lhs_nospaces;
    for (char c : lhs) {
        if (!std::isspace(c)) {
            lhs_nospaces += c;
        }
    }
    lhs = lhs_nospaces;

    string rhs_nospaces;
    for (char c : rhs) {
        if (!std::isspace(c)) {
            rhs_nospaces += c;
        }
    }
    rhs = rhs_nospaces;

    //Determining negative numbers
    bool lhs_negative = false;
    bool rhs_negative = false;
    if (lhs.find('-') != std::string::npos) {
        lhs_negative = true;
        if (lhs[0] == '-') {
            lhs = lhs.substr(1, lhs.length() - 1);
        }
    }
    if (rhs.find('-') != std::string::npos) {
        rhs_negative = true;
        if (rhs[0] == '-') {
            rhs = rhs.substr(1, rhs.length() - 1);
        }
    }

    int len_lhs = lhs.length(); //Find length of first string
    int len_rhs = rhs.length(); //Find length of second string

    //Determine max length of the 2 strings and set large number as top and small number as bottom
    if (len_lhs > len_rhs) {
        max_length = len_lhs;
        len_top = max_length;
        len_bottom = len_rhs;
        top_num = lhs;
        bottom_num = rhs;
    }
    if (len_rhs > len_lhs) {
        max_length = len_rhs;
        len_top = max_length;
        len_bottom = len_lhs;
        top_num = rhs;
        bottom_num = lhs;
    }
    if (len_lhs == len_rhs) {
        max_length = len_lhs;
        len_top = max_length;
        len_bottom = len_rhs;
        top_num = lhs;
        bottom_num = rhs;
    }

    for (int i = len_bottom - 1; i >= 0; i--) { //First for loop to iterate through the bottom number

        carry = 0;
        backwardsAnswer = "";
        for (int j = len_top -1 ; j >= 0; j--) { //Second iterates through the large top number

            multiply = ((digit_to_decimal(bottom_num[i]) * digit_to_decimal(top_num[j])) + carry);
            if (multiply > 9) {
                carry = multiply / 10;
                answer = multiply % 10;
            }
            else {
                carry = 0;
                answer = multiply;
            }
            backwardsAnswer += decimal_to_digit(answer);
        }

        if (carry != 0) { //If carry remains after the loop, add it as an additional digit to the end of the string
            backwardsAnswer += decimal_to_digit(carry);
        }
        int new_length = backwardsAnswer.length();
        for (int k = 0; k < new_length / 2; k++) { //Reverse the order of the string to get the correct order of digits
            swap(backwardsAnswer[k], backwardsAnswer[new_length - k -1]);
        }
        for (int x = 1; x <= (len_bottom - i - 1); x++) { //Append 0 to the number AFTER it swaps it
        backwardsAnswer += "0";
        }
        if (i == (len_bottom - 1)) { //If in the first iteration, set the answer to total
            total = backwardsAnswer;
        }
        else { //If in any other iteration add the first iteration with that one
            total = add(total, backwardsAnswer);
        }
    }
    
    if ((lhs_negative == true) && (rhs_negative == false)) { //if lhs is "-" and rhs is "+" number is negative
        final_answer = "-" + trim_leading_zeros(total);
    }
    else if ((lhs_negative == false) && (rhs_negative == true)) {
        final_answer = "-" + trim_leading_zeros(total);
    }
    else {
        final_answer = trim_leading_zeros(total);
    }
    return final_answer;
}
