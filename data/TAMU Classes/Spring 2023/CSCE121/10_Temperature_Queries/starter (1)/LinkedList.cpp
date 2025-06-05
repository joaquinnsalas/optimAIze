# include <iostream>
# include <string>
# include <sstream> // for the setting the percision
# include "LinkedList.h"
# include "Node.h"
# include <sstream>
using namespace std;
using std::string, std::ostream;

LinkedList::LinkedList() : head(nullptr), tail(nullptr) /* TODO */ { //default constructor
	// TODO: implement this function
}

LinkedList::~LinkedList() { //destructor
	// TODO: implement this function
	clear();
}

LinkedList::LinkedList(const LinkedList& source) : head(nullptr), tail(nullptr) /* TODO */ { //Copy constructor
	// TODO: implement this function
	// helper pointer
	// traverse the list
	Node* copycon = source.getHead();

	head = nullptr;
	tail = nullptr;

	// while marker points to a node, traverse the list
	while (copycon != nullptr) {

		Node* newnode = new Node;
		newnode->data = copycon->data;
		newnode->next = nullptr;

		if (head == nullptr) {
			head = newnode;
			tail = newnode;
		}
		else {
			// Insert the newnode as the last node
			tail->next = newnode;
			// assign newnode to the last node
			tail = newnode;
		}
		copycon = copycon->next;
	}
}

LinkedList& LinkedList::operator=(const LinkedList& source) { // copy assignment operator
	// TODO: implement this function
	// Self check
	if (this != &source) {
		clear();
		head = nullptr;
		tail = nullptr;

		Node* marker = source.head;
		while (marker != nullptr) {
			Node* newnode = new Node;
			newnode->data = marker->data;
			newnode->next = nullptr;

			if (head == nullptr) {
				head = newnode;
				tail = newnode;
			}
			else {
				tail->next = newnode;
				tail = newnode;
			}
			marker = marker->next;
		}
	}
	return *this;
}

void LinkedList::insert(string location, int year, int month, double temperature) {
	// TODO: implement this function
	// Allocate new linkedlist
	Node* newNode = new Node(location, year, month, temperature);
	// put in the new data
	newNode->data = TemperatureData(location, year, month, temperature);
	newNode->next = nullptr;

    // into empty list
    if (head == nullptr) {
        head = newNode;
        tail = newNode;
        return; 
    }

	Node* current = head; // this is to traverse the list
	Node* previous = nullptr; // the prev node

	// Skip all nodes whose number is smaller than value.
	while (current != nullptr && current->data < newNode->data) {
		previous = current;
		current = current->next;
	}
	// Inserting before the head
	if (current == head) {
		newNode->next = head;
		head = newNode;
	}
	// Inserting after the tail
	else if (previous == tail) {
		previous->next = newNode;
		tail = newNode;
	}
	// Inserting in the middle
	else {
		previous->next = newNode;
		newNode->next = current;
	}
}

void LinkedList::clear() {
	// TODO: implement this function
	Node* nodeclear = nullptr;
	//While head is not nullptr (from notes)
	while (nodeclear != nullptr) {
		//Save head pointer to marker
		nodeclear = head;
		//position head at the next node
		head = head->next;
		nodeclear->next = nullptr;
		delete nodeclear;	//Delete the node
	}
	head = nullptr;
	tail = nullptr;
	nodeclear = nullptr;
}

Node* LinkedList::getHead() const { return head; } // TODO: implement this function, it will be used to help grade other functions

string LinkedList::print() const {
	string outputString;
	stringstream ss;

	Node* marker = head; // get head and print it out

	while(marker != nullptr){
		ss << marker->data.id << " " << marker->data.year << " " << marker->data.month << " " << marker->data.temperature << endl;
		marker = marker->next;
	}

	outputString = ss.str();

	return outputString;
}

ostream& operator<<(ostream& os, const LinkedList& ll) {
	os << ll.print();
	return os;
}
