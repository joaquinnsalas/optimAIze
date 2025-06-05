#include <iostream>
using std::cout, std::endl;

struct Node {
  int value;
  Node* next;
  Node(int num = 0) : value(num), next(nullptr) {}
};

class LinkedList {
private:
  Node* head;

 public:
   // Constructor
   LinkedList() : head(nullptr) {}
   
   // Destructor
   ~LinkedList();
   
   // copy constructor
   LinkedList(const LinkedList& other);
   
   // copy assignment operator
   LinkedList & operator=(const LinkedList& other);
   
   // other member functions
   void clear();
   double average() const;
   void removeMax();
   void insertFront(int);
   void reverse();   
   void displayList() const;
   Node* middle() const;
   bool hasCycle() const;
   void appendNode(int num);
};

/*
Linked List Cycle
Write a member function of the class LinkedList that returns 
true if a cycle exists in the linked list, false otherwise.
*/
bool LinkedList::hasCycle() const
{
   if (head == nullptr) 
       return false;
   // use two pointers, which move through the list at different speeds
   Node* tortoise = head;
   Node* hare = head;
   while (tortoise != nullptr && hare != nullptr && hare->next !=nullptr) 
   {
       // at each step, move tortoise one step forward
      tortoise = tortoise->next;
      // at each step, move hare two steps forward
      hare = hare->next->next;
      // the idea is that if there is a cycle, the two pointers will meet
      // finally
      if (tortoise == hare) 
          return true;
   }
   return false;
}


/*
Middle of the List
Write a member function of the class LinkedList that returns 
a pointer to the element in the middle of the list (if the 
list has n elements, it should return a pointer to the 
([n/2]+1)-th element).
	Do not assume the existence of any other functions to use.
	Return nullptr if the list is empty.
*/
Node* LinkedList::middle() const
{
   int n = 0;
   Node* marker = head; 
   if (marker == nullptr) 
       return nullptr;
   // count number of nodes in list
   while (marker != nullptr) {
      marker = marker->next;
      ++n;
   }
   // the index of the middle node
   marker = head;
   for (int i=0; i < n/2; ++i)
      marker = marker->next;

   return marker;
}

/* 
LinkedList Average
Write a member function of the class LinkedList (a simply-linked list, with a pointer head to its first element) that returns the average of the elements in the list. 
*/
double LinkedList::average() const
{
   double sum = 0.0; 
   unsigned count = 0;
   Node* marker = head; 

   if (marker == nullptr) 
       throw "list empty\n";
   while (marker != nullptr) {
      sum += marker->value;
      marker = marker->next;
      ++count;
   }
   return sum/count;
}

void LinkedList::insertFront(int num) 
{
   Node *newNode = nullptr;

   // Allocate a new node & store num
   newNode = new Node;
   newNode->value = num;
   newNode->next = head;
   head = newNode;
}


//Remove a certain item in the list
void LinkedList::removeNum(int a) {

   if (head == nullptr)
      return;  // nothing to do
        
   Node* prev = nullptr;
   Node* marker = head;

   // traverse the list, removing all nodes with the given value
   while (marker != nullptr) {

      if (marker->value == a) {

         Node* temp = marker;
         // if the first node has the given value
         if (prev == nullptr) {
            head = marker->next;
            marker = head;
         }
         else {
            // link previous node to marker node's next node
            prev->next = marker->next;
            marker = marker->next;
         }
         delete temp;
      }
      else { // skip all nodes whose value member is not equal to a
         prev = marker;
         marker = marker->next;
      }
   }
}



/*
Remove all Maximum
Write a member function of the class LinkedList that removes from the list all occurrences of the maximum element in the list. 
*/
void LinkedList::removeMax()
{
   if (head == nullptr) 
       return;  // nothing to do
   
   // traverse the list to find the maximum value
   int max = head->value;
   Node* marker = head;
   while (marker != nullptr) {
      if (marker->value > max) 
          max = marker->value;
      marker = marker->next;
   }

   Node* prev = nullptr;
   marker = head;

   // traverse the list again, removing all max values
   while (marker != nullptr)
   {
       if (marker->value == max)
       {
           Node* temp = marker;
           // if the first node is a max
           if (prev == nullptr)
           {
               head = marker->next;
               marker = head;
           }
           else
           {
               // link previous node to marker node's next node
               prev->next = marker->next;
               marker = marker->next;
           }
           delete temp;
       }
       else  // skip all nodes whose value member is not equal to max
       {
           prev = marker;
           marker = marker->next;
       }
   }
}


void LinkedList::clear() // To clear the entire linkedlist
{
    Node* marker = nullptr;
    while (head != nullptr) {
        marker = head;
        head = head->next;
        delete marker;
   }
   head = nullptr;
}

LinkedList::~LinkedList() 
{
   cout << "Calling Destructor" << endl;
   clear();
}

//**************************************************
// Copy constructor                                *
//**************************************************
LinkedList::LinkedList(const LinkedList &other)
{
	Node *nodePtr = nullptr;

   // Initialize the head pointer.
	head = nullptr;

   // Point to the other object's head.
   nodePtr = other.head;

   // Traverse the other object.
   while (nodePtr)
   {
      // Append a copy of the other object's
      // node to this list.
      appendNode(nodePtr->value);

	  // Go to the next node in the other object.
      nodePtr = nodePtr->next;
   }
}

//**************************************************
// appendNode appends a node containing the        *
// value pased into num, to the end of the list.   *
//**************************************************

void LinkedList::appendNode(int num)
{
	Node *newNode, *nodePtr = nullptr;

   // Allocate a new node & store num
   newNode = new Node;
   newNode->value = num;
   newNode->next = nullptr;

   // If there are no nodes in the list
   // make newNode the first node
   if (!head)
      head = newNode;
   else  // Otherwise, insert newNode at end
   {
      // Initialize nodePtr to head of list
      nodePtr = head;

      // Find the last node in the list
      while (nodePtr->next)
         nodePtr = nodePtr->next;

      // Insert newNode as the last node
      nodePtr->next = newNode;
   }
}

//**************************************************
// Copy assignment operator                        *
//**************************************************

LinkedList &LinkedList::operator=(const LinkedList &other){
	
	if(this != &other){ // prevent self-copy


		if(other.head == nullptr) {
         head = nullptr;
      }
		else {
         clear();
         Node *nodePtr = nullptr;

         // Initialize the head pointer.
         head = nullptr;

         // Point to the other object's head.
         nodePtr = other.head;
         
         // Traverse the other object.
         while (nodePtr)
         {
            // Append a copy of the other object's
            // node to this list.
            appendNode(nodePtr->value);

            // Go to the next node in the other object.
            nodePtr = nodePtr->next;
         }
		}
	}
	return *this; 
}


void LinkedList::reverse()
{     
	Node  *newHead = nullptr,
         *newNode = nullptr,
         *marker = nullptr,
         *tempPtr = nullptr;

   // Traverse the list, building a copy of it in reverse order.
   marker = head;
   while (marker != nullptr) 
   {
      // Allocate a new node & store the value of the current list node in it.
      newNode = new Node(marker->value);
     // newNode->value = marker->value;
     // newNode->next = nullptr;
	  
      // Shift the existing nodes in the new list down one, inserting the new
      // node at the front.
      if (newHead != nullptr) 
      {
          // link new node to the prior head
          newNode->next = newHead;
          // update newHead
          newHead = newNode;
      }
      else 
      {
          newHead = newNode;
      }

	    // Go to the next node in the list.
      marker = marker->next;
   }
   // Destroy the existing list.
   clear();
   // Make he(marker->value)ad point to the new list.
   head = newHead;
}

void LinkedList::displayList() const
{
   Node *nodePtr;  // To move through the list
   // Position nodePtr at the head of the list.
   nodePtr = head;

   // While nodePtr points to a node, traverse
   // the list.
   while (nodePtr) {
      // Display the value in this node.
      cout << nodePtr->value << endl;

      // Move to the next node.
      nodePtr = nodePtr->next;
   }
}    

int main()
{

   LinkedList myList;
   
   myList.insertFront(6);
   myList.insertFront(1);
   myList.insertFront(2);
   myList.insertFront(6);
   myList.insertFront(3);
   myList.insertFront(0);   
   myList.insertFront(6);
   myList.insertFront(5);
   myList.insertFront(4);
   myList.insertFront(6);
  
   cout << "Here is the list:" << endl;
   myList.displayList();

   cout << "Here is the list after reversing:" << endl;
   myList.reverse();
   myList.displayList();
   
   try {
      cout << "Average value: " << myList.average() << endl;
   }
   catch (char const * msg) {
      cout << msg << endl;
   }
   
   myList.removeMax();
   myList.displayList();
   
   cout << "middle value: " << (myList.middle())->value << endl;
   
   if (myList.hasCycle()) 
      cout << "List has a cycle" << endl;
   else
      cout << "List has no cycle" << endl;
   
   // head ptr made public so we can do this
   (myList.middle())->next->next = myList.middle();  
   if (myList.hasCycle()) {
      cout << "List has a cycle" << endl;
      exit(-1);
   }
   else
      cout << "List has no cycle" << endl;   
}
