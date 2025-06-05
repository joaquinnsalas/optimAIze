// TODO: Implement this source file
# include <iostream>
# include <stdexcept>

# include "MyString.h"

using std::ostream;
// Default Constructor
MyString::MyString() : size_(0), capacity_(20), str(new char[20]) { //Constructs an empty string, with a length of zero characters 
    for (size_t i = 0; i < this->capacity_; i++) {
        this->str[i] = '\0'; //fill it will null
    }
}
//Parameterized constructor
MyString::MyString(const char* s) : size_(0), capacity_(20), str(nullptr) {
    if (s == nullptr) {
        this->str = new char[1];
        this->str[0] = '\0';
        return;
    }
    // Copy letters fdrom the string until hits null
    size_t c = 0;
    while (s[c] != '\0') {
        c++;
    }
    this->size_ = c;
    while (this->size_ > this->capacity_) { //for resizing
        this->capacity_ *= 2;
    }
    this->str = new char[this->capacity_];
    for (size_t i = 0; i < this->capacity_; ++i) {
        if (i < this->size_) {
            this->str[i] = s[i];
        } else {
            this->str[i] = '\0';
        }
    }
}

//                                     THE RULE OF THREE (Destructor, Copy Constructor, Copy Assignment Operator)
// Destructor
MyString::~MyString() { // From TA notes
    // 1: deallocate memory
    delete[] this->str;
    // 2: handle dangling pointers
    this->str = nullptr;
    this->size_ = 0;
    this->capacity_ = 2; //maybe 20 is too much?
}
/*
MyString::~MyString() {
    // first deallocate memory
    delete[] array;
    // and than handle dangling pointers
    array = nullptr;
    size = 0;
    capacity = 0;
}
*/
//Copy constructor
MyString::MyString(const MyString& str) : size_{str.size_}, capacity_{str.capacity_}, str{nullptr} {
    // Step 1: Allocate memory
    this->str = new char[this->capacity_];
    // Step 2: Copy the values
    for (size_t i = 0; i < this->size_; i++) { //Maybe my memory error is here, loop in range of size instead of capacity
        this->str[i] = str.at(i); //copy values
    }
    this->str[size_] = '\0'; //add null char to end
}
/*
MyString::MyString(const MyString& example) {
    
    size = example.size;
    capacity = example.capacity;

    // Step 1: Allocate memory
    array = new int[capacity];

    // Step 2: Copy the values
    for (int i = 0; i < size; i++) {
        array[i] = example.array[i];
    }
}
*/
// Copy Assignemnt Opertator from TA notes
MyString& MyString::operator=(const MyString& original) {

    this->size_ = original.size_;
    this->capacity_ = original.capacity_;
    // 1: self assignment check
    if (this != &original) {
        // 2: deallocate memory
        delete[] this->str;
        // 3: allocate memory
        this->str = new char[this->size_ + 1];
        // 4: copy values
        for (size_t i = 0; i < this->capacity_; i++) {
            this->str[i] = original.str[i];
        }
        this->str[this->size_] = '\0'; //add null char at the end 
    }
    return *this;
}
/*
MyArray& MyArray::operator=(const MyArray& other) {

    // Step 1: self-assignment check
    if (this != &other) {

        // Step 2: deallocate memory
        delete[] arr;

        // Step 3: allocate memory
        capacity = other.capacity;
        arr = new int[capacity];

        // Step 4: copy values
        size = other.size;
        for (int i = 0; i < size; i++) {
            arr[i] = other.arr[i];
        }
    }
    // Step 5: return self
    return *this;
}
*/
void MyString::resize(size_t number) { //add more to the array

// 1 - check if the array needs to be resized
    // 2 - if the array needs to be resized:
    if (size_ == capacity_) { 
        // allocate a new array with double the current capacity
        int* new_arr = new int[capacity_ * 2];
        // copy the values from the old array to the new array
        for (int i = 0; i < size_; i++) {
            new_arr[i] = str[i];
        }
        // update the capacity of the dynamic array
        capacity_ *= 2;
        // deallocate the memory used by the old array
        delete[] str;
        // set the pointer of the old array to the pointer of the new array
        //str = new_arr;
    }
    // add the new value to the dynamic array
    str[size_] = number;
    size_++;
}
//                                                                    Getters

// void MyString::resize(int a) { //to remove a item from a linkedlist
//    if (head == nullptr)
//       return;  // nothing to do
        
//    Node* prev = nullptr;
//    Node* marker = head;

//    // traverse the list, removing all nodes with the given value
//    while (marker != nullptr) {

//       if (marker->value == a) {

//          Node* temp = marker;
//          // if the first node has the given value
//          if (prev == nullptr) {
//             head = marker->next;
//             marker = head;
//          }
//          else {
//             // link previous node to marker node's next node
//             prev->next = marker->next;
//             marker = marker->next;
//          }
//          delete temp;
//       }
//       else { // skip all nodes whose value member is not equal to a
//          prev = marker;
//          marker = marker->next;
//       }
//    }
// }

size_t MyString::size() const noexcept { return this->size_; } //moore said to keep these on one line

size_t MyString::capacity() const noexcept { return this->capacity_; } //noexcept from cpp website

size_t MyString::length() const noexcept { return this->size_; }

const char* MyString::data() const noexcept { return this->str; }

const char& MyString::front() const { return this->str[0]; }

bool MyString::empty() const noexcept { return this->size_ == 0; }

const char& MyString::at(size_t index) const {
    if (index >= this->size_) {
        throw std::out_of_range("Index is noooo good");
    }
    return this->str[index];
}

size_t MyString::find(const MyString& s, size_t pos) const noexcept {
    if (pos >= this->size_) {
        return -1;
    }
    for (size_t i = pos; i < (this->size_ - s.size()) + 1; i++) { //since starting at 0. its going to start at the position
        bool find = true;

            for (size_t j = 0; j < s.size(); j++) { //iterate through that position
                if (str[i + j] != s.at(j)) { //had to change, forgot what i was doin
                    find = false;
                    break;
                }
            }
        if (find) {
            return i;
        }
    }
    return -1;
}
//                                                                    Setters

void MyString::clear() noexcept {
    //Erases the contents of the string, which becomes an empty string (with a length of 0 characters).
    delete[] this->str;
    str = new char[1];
    str[0] = '\0'; //null char
    this->size_ = 0; //no size, capacity is 1
    this->capacity_ = 1;
}
//                                                                    Operators

MyString& MyString::operator+= (const MyString& s) { //had the wrong thing here
    size_t firstsize = this->size_;
    size_t secondsize = s.size();
    size_t need = firstsize + secondsize;

    if (need > this->capacity_) {
        size_t newcapacity = need * 2;
        char* newstr = new char[newcapacity]; //Allocate new memory
        for (size_t i = 0; i < firstsize; i++) { //load into the jwn from 0-whereever the string ends
            newstr[i] = this->str[i];
        }
        for (size_t i = 0; i < secondsize; i++) { //from wherever the string ends to end
            newstr[i + firstsize] = s.at(i); //changed this to fill out the second part of the str
        }
        newstr[need] = '\0'; //add the null char

        delete[] this->str; //release memory
        this->str = newstr; //from the allocating new memory notes
        this->size_ = need; 
        this->capacity_ = newcapacity; //if theres a probelm i need to make a new var for capacity
    } else {
        for (size_t i = 0; i < secondsize; i++) { //edge case that took FOREVER to figure out
            this->str[i + firstsize] = s.at(i);
        }
        this->size_ = need;
        this->str[need] = '\0';
    }
    return *this;
}

ostream& operator<<(ostream& os, const MyString& str) {
    for (size_t i = 0; i < str.size(); i++) { //just print out ever char in the str
        os << str.at(i);
    }
    return os;
} 

bool operator==(const MyString& lhs, const MyString& rhs) noexcept {

    bool istrue = true;
    if (lhs.size() != rhs.size()) { //compare lengths first
        istrue = false; 
    }
    else {
        for (size_t i = 0; i < rhs.size(); ++i) { //compare chars next // still not passing some test cases
            if (lhs.at(i) != rhs.at(i)) {
                istrue = false;
                break;
            }
        }
    }
    return istrue;
}

MyString operator+ (const MyString& lhs, const MyString& rhs) { //not working for som test cases
    MyString answer = lhs; //get lefthand side as whattoreturn
    answer += rhs; 
    return answer; 
}

void MyString::resize(size_t n) {

    char* newstr = new char[n + 1]; // make a new string with the resized value
    size_t i;
    for (i = 0; i < n && i < this->capacity_; i++) { //load those chars into the new string
        newstr[i] = this->str[i];
    }
    newstr[i] = '\0'; // after, add the null at the end
    //and update everything after (peer teacher helped)
    delete[] this->str; // free memory
    this->str = newstr; // set equal to new str
    this->size_ = i;
    this->capacity_ = n; 
}