#include <iostream>
using namespace std;

int main()
{
    int a[11] = {5, 2, 2, 3, 4, 4, 4, 4, 1, 1, 1};
    int n = 11;
    int count = 1;
    int i = 1;

    //the idea is to count how many pairs (a[i-1], a[i]) such that a[i-1]!=a[i]
    //suppose we have count many such pairs, then we have count + 1 segments
 
    //iterate over the array and count how many such kind of pairs
    while (i < n)
    {
        if( a[i] != a[i-1] )
            count ++; 
        i++;
    }
    cout << "The sequence has " << count << " segements." << endl;

    return 0;
}
