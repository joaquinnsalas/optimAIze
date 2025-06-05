#include <iostream>

using namespace std;

//                                  Q2.1

float* AllocatorFloat::giveFloat(float val) {
    //Allocate memory for an element of float on the heap assigned to be logically equal to val
    // if it is nullptr, resize to contain only one element
    if (mem == nullptr) {
        capacity = 1;
        // also size should be 1
        size = 1;
        // only allocating memory, i am not adding anything into here
        float* new_mem = new float[capacity]; // with a capacity of 1
    }
    if (size == capacity) { // check if mem needs to be resized at all
        // allocate with double capacity
        float* new_mem = new float[capacity * 2];
        //copy values into the new one that is larger
        for (int i = 0; i < this->getSize(); i++) {
            new_mem[i] = mem[i];
        }
        // update the capacity of the dynamic float array
        capacity = capacity * 2;
        // deallocate the string
        delete [] mem;
        // set the pointer from the old array to that of the new one
        mem = new_mem;
        //pointer values must be set to nullptr if not being used
        new_mem = nullptr; //new_mem is no longer being used here
    }
    // use the old size to know where the last item is in the array
    // and that say that last item is now that item
    mem[size] = val;
    size++; // add one to the size

    // the pointer is the one returned
    return mem;
}

