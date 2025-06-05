#include <iostream>

int Largest(int a, int b, int c) {
  int d = a;
  if (b > d) {
    d = b;
  } 
  if (c > d) {
    d = c;
  }
  return d;
}

bool SumIsEven(int a, int b) {
  if (((a + b) % 2) == 0) {
    return true;
  }
return false;
}

int BoxesNeeded(int apples) {
  if (((apples % 20) == 0) && (apples > 0)) {
    return (apples / 20);
  }
  if (((apples % 20) != 0) && (apples > 0)) {
    return (apples / 20) + 1;
  }
return 0;
}

bool SmarterSection(int A_correct, int A_total, int B_correct, int B_total) {
  if ((A_correct < 0) || (A_total <= 0) || (B_correct < 0) || (B_total <= 0)) {
    throw std::invalid_argument("Invalid Argument.");
  }
  if ((A_correct > A_total) || (B_correct > B_total)) {
    throw std::invalid_argument("Invalid Argument.");
  }
return ((double(A_correct) / A_total) > (double(B_correct) / B_total));
}

bool GoodDinner(int pizzas, bool is_weekend) {
  if ((pizzas >= 10) && (pizzas <= 20) && (is_weekend == false)) {
    return true;
  }
  else if ((pizzas >= 10) && (is_weekend == true)) {
    return true;
  }
return false;
}

int SumBetween(int low, int high) {

  if (low > high) {
    throw std::invalid_argument("Invalid Argument.");
  }
  if (low == high) { //Just return the low integer. Ex. 5 & 5, answer is 5
    return high;
  }
  if (-low == high) { //Numbers will just cancel out
    return 0;
  }
  if ((low + high) == -1) { // If 4 & -5, return 4
    return low;
  }
  if ((low + high) == 1) { //If -5 & 6 return 6
    return high;
  }
  if ((low == INT32_MIN) && (high == INT32_MAX)) {
    return INT32_MIN;
  }
  if ((low < 0) && (high > 0)) {
    low = -low; // Turn low into a positive number
    if (low > high) {
      int newhigh = low;
      low = high;
      high = newhigh;
    }
    low++;
  }
  if (low == high) { 
    return low;
  }
  else if ((low * -1) == high) {
    return 0;
  }

  int value = 0;
  for (int n = low; n <= high; n++) {
    value += n;
    //Prevent from infinite loops in the for loop
    if ((n > 0) && (value > INT32_MAX - n)) { 
    throw std::overflow_error("Overflow Error.");
    }
    if ((n < 0) && (value < INT32_MIN - n)) {
      throw std::overflow_error("Overflow Error.");
    }
  }
  // if ((high - low) > 0) {
  //   if (high > 0) {
  //     if (INT32_MAX - high < low) {
  //       throw std::overflow_error("Overflow Error.");
  //     }
  //   }
  //   else {
  //     if (INT32_MIN - low > high) {
  //       throw std::overflow_error("Overflow Error.");
  //     }
  //   }
  // }
  // else {
  //   if (low < 0) {
  //     if (INT32_MIN - low > high) {
  //       throw std::overflow_error("Overflow Error.");
  //     }
  //   } else {
  //     if (INT32_MAX - high < low) {
  //       throw std::overflow_error("Overflow Error.");
  //     }
  //   }
  // }
  // }
  return value;
}


int Product(int a, int b) {
  if ((((INT32_MIN == a) && (b == -1))) || ((INT32_MIN == b) && (a == -1))) {
    throw std::overflow_error("Product overflow.");
  }

  if ((b > 0) && ((a > (INT32_MAX / b)) || (a < (INT32_MIN / b)))) {
    throw std::overflow_error("Product overflow.");
  }
  else if ((b < 0) && ((a < (INT32_MAX / b)) || (a > (INT32_MIN / b)))) {
    throw std::overflow_error("Product overflow.");
  }
return a * b;
}