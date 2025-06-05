#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main() {
    string userInput;
    istringstream inpt;
    string lhs;
    string rhs;
    string addition;
    
    cout << ">>" << endl;
    getline(cin, userInput);
    inpt.str(userInput);

    inpt >> lhs >> addition >> rhs;

    cout << lhs << endl;
    cout << rhs << endl;

    return 0;
}