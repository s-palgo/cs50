#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    string input = argv[1];

    bool keyisaninteger;

    for (int i = 0; i < strlen(input); i++)
    {
        if (isdigit(input[i]))
        {
            keyisaninteger = true;
        }
        else
        {
            keyisaninteger = false;
        }
    }

    string text;

    if (keyisaninteger)
    {
        text = get_string("Please input your text: \n");
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    int k = atoi(input);

    int key = k % 26;

    int ALPHABET[26] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25};

    for (int i = 0; i < strlen(text); i++)
    {
        if (isupper(text[i]))
        {
            int upper = text[i] - 'A';
            text[i] = ((ALPHABET[upper] + key) % 26) + 'A';
        }
        else if (islower(text[i]))
        {
            int lower = text[i] - 'a';
            text[i] = ((ALPHABET[lower] + key) % 26) + 'a';
        }
        else
        {
            text[i] = text[i];
        }
    }
    printf("ciphertext: %s\n", text);
    return 0;

    //printf("%s\n", text);
    // printf("Encryption: %s", text);
}