#include <iostream>
using namespace std;

void replace(char word[], int nums[], int size)
{
    int i = 0;
    int len = 0;

    while (word[len] != '\0')
        len++;

    for (i = 0; i < size; i++)
    {
        int index = 0;
        if (nums[i] > len)
            index = nums[i] % len;
        else
            index = nums[i];
        word[index] = '*';
    }
    cout << word << endl;
}

int main()
{
    char word1[] = "coffeehouseinTokyo";
    int nums1[] = {43, 11, 16};
    replace(word1, nums1, 3);

    char word2[] = "Hello my friends!";
    int nums2[] = {4, 19, 13, 10};
    replace(word2, nums2, 4);
    return 0;
}
