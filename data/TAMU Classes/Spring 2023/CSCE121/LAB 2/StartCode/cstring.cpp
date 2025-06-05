#include <iostream>
#include "cstring.h"

unsigned int length(char str[]) {
  // returns the length of the string including zero (0)
  int i = 0;
  while(str[i] != 0) {
    i++;
  }
  return i;
}

unsigned int find(char str[], char character) {
  // returns 
  int i = 0;
  while(str[i] != 0) {
    if (str[i] == character) {
      return i;
    }
  i++;
  }
  //  - the index of the first occurence of character in str
  //  - the size if the character is not found
  return i;
}

bool equalStr(char str1[], char str2[]) {
  // returns true if they are equal and false if they are not
  int i = 0;
  if (length(str1) != length(str2)) {
    return false;
  }
  while((str1[i] && str2[i]) != '\0') {
    if (str1[i] != str2[i]) {
      return false;
    }
  i++;
  }
  return true;
}