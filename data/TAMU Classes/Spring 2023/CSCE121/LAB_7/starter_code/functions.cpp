#include "functions.h"
using std::cin, std::cout, std::endl, std::ostream, std::string;

#define INFO(X)  cout << "[INFO] ("<<__FUNCTION__<<":"<<__LINE__<<") " << #X << " = " << X << endl;
#define INFO_STRUCT(X) cout << "[INFO] ("<<__FUNCTION__<<":"<<__LINE__<<") " << #X << " count = " << X.count << endl;

/**
 * ----- REQUIRED -----
 * Pushes number to top of stack. If stack is full, then resize stack's array.
 * @param   stack   Target stack.
 * @param   number  Number to push to stack.
 */
void push(Stack& stack, int number) {
  // TODO: implement push function for stack
  if (stack.capacity == stack.count) {
    int* newArray = new int[stack.capacity * 2]; //Access the capacity

    for (int i = 0; i < stack.capacity; i++) {
      newArray[i] = stack.numbers[i];
    }
    delete [] stack.numbers;
    stack.numbers = newArray;
    stack.capacity = stack.capacity * 2;
  }
  stack.numbers[stack.count] = number;
  stack.count = stack.count + 1;
  INFO_STRUCT(stack);
  INFO(number);
}

/**
 * ----- REQUIRED -----
 * Pops number from top of stack. If stack is empty, return INT32_MAX.
 * @param   stack   Target stack.
 * @return          Value of popped number.
 */
int pop(Stack& stack) {
  // TODO: implement pop function for stack
  int temp;
  if (stack.count == 0) {
    return INT32_MAX;
  }
  temp = stack.numbers[stack.count - 1];
  stack.count = stack.count - 1;

  INFO_STRUCT(stack);
  return temp;
}

/**
 * ----- REQUIRED -----
 * Returns the number at top of stack without popping it. If stack is empty, return INT32_MAX.
 * @param   stack   Target statck.
 * @return          Number at top of stack.
 */
int peek(const Stack& stack) {
  // TODO: implement peek function for stack
  int peek;
  peek = stack.numbers[stack.count - 1];
  INFO_STRUCT(stack);
  return peek;
}
