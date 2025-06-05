/*
Name and UIN
Write a complete C++ program that prints your name and UIN to standard output.
Example output:
Firstly Lastington
420006969
*/
#include <iostream>
using namespace std;

//my struct variable
struct student{
// make a string for name
string name;
// make a string for name
int UIN;
};

int main(void) {

    //first i need to call out a variable using me
    struct student me;
    //My name
    me.name = "Joaquin Salas";
    me.UIN = 731000141;
    cout << "First and Last name: " << me.name << endl;
    cout << "UIN: " << me.UIN << endl;
    return 0 ;
}
