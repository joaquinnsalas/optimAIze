#include <iostream>

using namespace std;

//                          Q2.2

//Rule of three (Destructor, Copy Constructor, Copy Assignment Operator)
// Destructor
AllocatorFloat::~AllocatorFloat() {
    //deallocate memory, here I can call the clear function in the starter code
    clear();
}

// Copy Constructor
AllocatorFloat::AllocatorFloat(const AllocatorFloat& mem) : mem(nullptr), size(mem.size), capacity(mem.capacity) {
    //allocate memory
    size = mem.size;
    capacity = mem.capacity;

    //allocate memory by creating a new array
    newmem = new float[capacity];

    // copy the values
    for (int i = 0; i < this->getSize(); i++) {
        newmem[i] = mem[i];
    }
}

// Copy Assignment Operator
AllocatorFloat& AllocatorFloat::operator=(const AllocatorFloat& other) {
    // first, self assignment check. no need fo it to equal its self
    if (this != &other) {
        // deallocate memory
        delete [] mem;
        //allocate new memory
        capacity = other.capacity;
        size = other.size;
        mem = new float[capacity];
        //copy over the same values
        for (int i = 0; i < this->getSize(); i++) {
            mem[i] = other.mem[i];
        }
    }
    //returns itself
    return *this;
}