#include <iostream>

using namespace std;

//                                Q3

void LinkedList::filterAnimal(std::string f) {
    //find a remove all nodes matching value from the linked list
    if (head == nullptr) {
        return; //here there is nothing to do
    }

    //make a node for the next and previous, set next to head and prev to null
    Node* previous = nullptr;
    Node* other = head;
    //check that while next is not null,
    while (other != nullptr) {
        if (other == f) {
            Node* holder = other; //this holder will get the value and be deleted later
        
            // if next is equal to the string f coming in than
            // make a temporary node,
            // here, rearrange the items in the list for different cases
            if (previous == nullptr) { //if its the last item in the list 
                // set that item to the head
                head = other->next;
                other = head;
            } else {
                // same thing, only rearranging
                // set the item next to it as the head
                prev->next = other->next;
                other = other->next;
            }
            delete holder; // delete the temporary holder to make sure of no memory leaks
        }
        else { // just skip all the nodes that the value does not equal string f
            previous = other;
            other = other->next;
        }
    }

}