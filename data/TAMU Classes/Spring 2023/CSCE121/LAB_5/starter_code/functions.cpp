# include "functions.h"
#include <iostream>
// add any includes

using std::cout, std::cin, std::endl, std::string;
using namespace std;

void deobfuscate() {
    string details;
    string input;
    cout << "Please enter obfuscated sentence: ";
    cin >> input;
    cout << "Please enter deobfuscation details: ";
    cin >> details;
    int index = 0;
    //int len = input.size();
    int len = details.size();
    for (int i = 0; i < len; i++) {
        if (i >= len) {
            break;
        }
        index += details.at(i) - '0';
        input.insert(index, " ");
        index += 1;
    }
    cout << "Deobfuscated sentence: " << input << endl;
    // TODO
}

void wordFilter() {
    string sentence, filterWord;
    cout << "Please enter the sentence: ";
    getline(cin, sentence);
    cout << "Please enter the filter word: ";
    cin >> filterWord;

    int sentenceLength = sentence.length();
    int filterLength = filterWord.length();
    bool foundWord = false;
    for (int i = 0; i < sentenceLength; i++) {
        if (isalpha(sentence.at(i))) {
            if (sentence.substr(i, filterLength) == filterWord) {
                foundWord = true;
                for (int j = i; j < i + filterLength; j++) {
                    sentence.at(j) = '#';
                }
            }
        }
    }
    if (!foundWord) {
        cout << "The word \"" << filterWord << "\" was not found in the sentence." << endl;
    }
    cout << "Filtered sentence: " << sentence << endl;
    // TODO
}

void passwordConverter() {
    // TODO
}

void wordCalculator() {
    // TODO
}

void palindromeCounter() {
    // TODO
}