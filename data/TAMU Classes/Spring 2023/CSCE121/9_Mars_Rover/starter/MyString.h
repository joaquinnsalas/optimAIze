// TODO: Implement this header file
#ifndef MYSTRING_H
#define MYSTRING_H

# include <iostream>

using std::ostream; //Use later for "<<"

class MyString {

    private:

        //do not initialize here, it slows down the program
        unsigned int size_;     //Size for items added to the dynamic array of chars
                                //underscore keeps it from being like .size()
        unsigned int capacity_; //Number of items the array can currently hold
        char* str;

    public: //API

        MyString(); //Default constructor

        MyString(const char* s); //Parameterized constructor

        // The big three
        ~MyString(); //Destructor
        MyString(const MyString& str); // Copy constructor
        MyString& operator=(const MyString& original); //Copy assignemnt operator //thank you dr professor

        // getters
        size_t size() const noexcept; //Ones that you can fit in a line will go here like this, on the other file
        size_t capacity() const noexcept;
        size_t length() const noexcept;
        bool empty() const noexcept;
        const char& front() const;
        const char* data() const noexcept;
        const char& at(size_t index) const;
        void clear() noexcept;
        size_t find(const MyString& s, size_t pos = 0) const noexcept; //not sure which to use
        void resize(size_t n);

        // Other operators
        friend ostream& operator<<(ostream& os, const MyString& str);
        MyString& operator+= (const MyString& s);

        //Maybe extra cred
        friend bool operator==(const MyString& lhs, const MyString& rhs) noexcept; //bringing in strings
        // friend MyString operator+(const MyString& lhs, const MyString& rhs);
};
# endif
