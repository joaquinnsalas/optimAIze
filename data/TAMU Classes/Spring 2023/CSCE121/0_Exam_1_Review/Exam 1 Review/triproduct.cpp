#include <iostream>
using namespace std;

bool isTriproduct(int n)
{
    int i = 1;

    while (i * (i + 1) * (i + 2) <= n)
    {
        if (i * (i+1) * (i + 2) == n)
            return true;
        i++;
    }

    return false;
} 

int main()
{
    int n;
    cin >> n;
    
    if (isTriproduct(n))
        cout << n << " is triproduct." << endl;
    else
        cout << n << " is not triproduct." << endl;
    return 0;
}
