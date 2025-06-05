# include "linked_list.h"
# include <iostream>
# include <string>

using std::cout, std::endl, std::string, std::ostream;

void MyList::add(const std::string& name, int score) {
    // TODO
    MyNode* newNode = new MyNode(name, score);

    if (_head == nullptr) {
        _head = newNode;
        _tail = newNode;
        this->_size += 1;
    }
    else {
        _tail->next = newNode;
        newNode->prev = _tail;
        _tail = newNode;
        this->_size += 1;
    }
}

void MyList::clear() {
    // TODO
    MyNode* nodeClear = _head;

    while(nodeClear != nullptr) {
        MyNode* nextNode = nodeClear->next;
        delete nodeClear;
        nodeClear = nextNode;
    }
    _head = nullptr;
    _tail = nullptr;
    _size = 0;
}

bool MyList::remove(const std::string& name) {
    // TODO
    MyNode* newNode = _head;
    while (newNode != nullptr) { //While not a nullptr or end of a list
        if (newNode->name == name) { //Compare it to the name in the current pointing of the linkedlist
            if (newNode == _head) { //If found and it is the head
                _head = newNode->next;
                _head->prev = nullptr; //Delete that position
            }
            else {
                newNode->next->prev = newNode->prev; 
            }
            if (newNode == _tail) {
                _tail = newNode->prev;
                _tail->next = nullptr;
            }
            else {
                newNode->prev->next = newNode->next;
            }
            delete newNode;
            _size--;
            return true;
        }
        newNode = newNode->next;
    }
    return false;
}

bool MyList::insert(const std::string& name, int score, size_t index) {
    // TODO
    // Create a new node with the given name and score
    MyNode* newNode = new MyNode(name, score);
    
    // Special case, inserting at the beginning of the list
    if (index == 0) {
        newNode->next = _head;
        newNode->prev = nullptr;
        if (_head != nullptr) {
            _head->prev = newNode;
        }
        _head = newNode;
        if (_tail == nullptr) {
            _tail = newNode;
        }
        _size++;
        return true;
    }

    // Traverse the list to find the node at the given index
    MyNode* currentNode = _head;
    size_t currentIndex = 0;
    while (currentNode != nullptr && currentIndex < index) {
        currentNode = currentNode->next;
        currentIndex++;
    }
    
    // If the index is out of bounds, return false
    if (currentNode == nullptr) {
        delete newNode;
        return false;
    }
    
    // Insert the new node before the current node
    newNode->prev = currentNode->prev;
    newNode->next = currentNode;
    if (currentNode->prev != nullptr) {
        currentNode->prev->next = newNode;
    }
    currentNode->prev = newNode;
    if (currentNode == _head) {
        _head = newNode;
    }
    _size++;
    return true;
}

MyList::MyList() : _size(0), _head(nullptr), _tail(nullptr) {} // Constructor

MyList::~MyList() { //Destructor
    clear();
}

size_t MyList::size() const { return _size; }

bool MyList::empty() const { return _head == nullptr; }

MyNode* MyList::head() const { return _head; }

ostream& operator<<(ostream& os, const MyList& myList) {
    MyNode* _current = myList.head();
    if (_current == nullptr) {
        os << "<empty>" << endl;
        return os;
    }

    os << "[ " << _current->name << ", " << _current->score << " ]";
    _current = _current->next;
    while (_current != nullptr) {
        os << " --> [ " << _current->name << ", " << _current->score << " ]";
        _current = _current->next;
    }
    
    return os;
}

MyNode::MyNode(const std::string& name, int score) : name{name}, score{score}, next{nullptr}, prev{nullptr} {}
