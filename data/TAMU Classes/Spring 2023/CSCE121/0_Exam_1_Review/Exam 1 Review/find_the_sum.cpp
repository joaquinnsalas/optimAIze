#include <iostream>
using namespace std;

int main()
{
    int a[5000] = {1, 2, 3, 4, 5, 6, 7, 8};
    int n = 8, k = 8;
    bool flag = false;
    
    for (int i = 0; i < n; i++)
    {
        for (int j = i + 1; j < n; j++)
        {
            if (a[i] + a[j] == k)
            {
                cout << a[i] << "  " << a[j] << endl;
                flag = true;
                break;
            }
        }
    }

    if (!flag)
        cout << "none" << endl;

    return 0;
}
