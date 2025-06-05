#include <iostream>
#include <ctype.h>
using namespace std;

bool isVowel(char ch)
{
    ch = tolower(ch);
    if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u' || ch == 'y')
        return true;
    return false;
}

int moreImportant(char word1[], char word2[])
{
    int len1 = 0, len2 = 0;
    int i = 0;
    while (word1[len1] != '\0')
        len1 ++;
    while (word2[len2] != '\0')
        len2 ++;

    int weight1 = 0, weight2 = 0;

    for (i = 0; i < len1 && i < len2; i++)
    {
        bool flag1 = isVowel(word1[i]);
        bool flag2 = isVowel(word2[i]);

        if (flag1 == true && flag2 == false)
            weight1 += 3;
        else if (flag1 == true && flag2 == true || flag1 == false && flag2 == false)
        {
            if (tolower(word1[i]) < tolower(word2[i]))
                weight2 += 1;
            if (tolower(word1[i]) > tolower(word2[i]))
               weight1 += 1; 
        }
        else // (flag1 == false && flag2 == true)
            weight2 += 3;
    }
    if (len1 < len2)
    {
        for (i = len1; i < len2; i++)
        {
            if (isVowel(word2[i]))
                weight2 += 2;
            else
                weight2 += 1;
        }
    }
    if (len1 > len2)
    {
        for (i = len2; i < len1; i++)
        {
            if (isVowel(word1[i]))
                weight1 += 2;
            else
                weight1 += 1;
        }
    }
    if (weight1 > weight2)
        return 1;
    else if (weight1 < weight2)
        return 2;
    else
        return 0;
}


int main()
{
    char word1[100], word2[100];
    cout << "Please enter two words: ";
    cin >> word1 >> word2;
    cout << moreImportant(word1, word2) << endl;
    return 0;
}
