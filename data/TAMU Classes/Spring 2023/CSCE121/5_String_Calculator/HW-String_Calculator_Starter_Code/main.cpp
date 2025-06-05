#include <iostream>
#include <string>
#include <limits>
#include "./string_calculator.h"

using std::cout, std::endl, std::cin;
using std::string;

int main() {
    cout << "String Calculator" << endl;
    cout << "\"q\" or \"quit\" or ctrl+d to exit" << endl;
    cout << ">> " << endl;
    // TODO(student): implement the UI
    string inpt, rhs, lhs, answer;

    while (getline(cin, inpt)) {

        if ((inpt == "q") || (inpt == "quit") || cin.eof()) {
            cout << "farvel!" << endl;
            break;
        }
        else if (inpt.find('+') != std::string::npos) { // Extract the left-hand side (lhs) and right-hand side (rhs) of the input string

            lhs = inpt.substr(0 , inpt.find('+')); //Determine is this addition or multiplication using string.find()
            rhs = inpt.substr(inpt.find('+') + 1);
            answer = add(lhs, rhs);
            cout << "ans = " << endl << endl;
            cout << "    " << answer << endl << endl;
            cout << ">> " << endl;
        }
        else if (inpt.find('*') != string::npos) { //finds the position of the symbol

            lhs = inpt.substr(0 , inpt.find('*')); //Takes everything from the left
            rhs = inpt.substr(inpt.find('*') + 1); //Takes everything from the right
            answer = multiply(lhs, rhs);
            cout << "ans = " << endl << endl;
            cout << "    " << answer << endl << endl;
            cout << ">> " << endl;
        }
        else if (inpt.find('-') != string::npos) {

            lhs = inpt.substr(0 , inpt.find('-')); //Takes everything from the left
            rhs = inpt.substr(inpt.find('-') + 1); //Takes everything from the right
            cout << ">>" << endl;
            cout << "ans = " << endl << endl;
            //cout << "   " << answer << endl << endl;
            cout << ">> ";
        }
    }
    return 0;
}
