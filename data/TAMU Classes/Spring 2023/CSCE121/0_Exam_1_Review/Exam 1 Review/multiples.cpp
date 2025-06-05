#include <iostream>
using namespace std;

int main()
{
    int n, k, l;
    cin >> n >> k >> l;
    int i = 0, d1 = 1, d2 = 1;

    // the numbers that are multiple of k are {k, 2*k, 3*k, ..., n*k}
    // the numbers that are multiple of l are {l, 2*l, 3*l, ..., n*l}
    // the solution should be the n smallest numbers of the above two sets 

    for (i = 0; i < n; i++)
    {
        if (d1 * k < d2 * l)
        {
            cout << d1*k << "  ";
            d1 ++;
        }
        else if (d1 * k == d2 * l)
        {
            cout << d1 * k << "  ";
            d1 ++; 
            d2 ++;
        }
        else
        {
            cout << d2 * l << "  ";
            d2++;
        }
    }
    cout << endl;
    return 0;
}
