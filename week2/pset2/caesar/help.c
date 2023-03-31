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
    }
    string input = argv[1];

    bool isvalidkey;

    for (int i = 0; i < strlen(input); i++)
    {
        if (isdigit(input[i]))
        {
            isvalidkey = true;
        }
        else
        {
            isvalidkey = false;
        }
    }

    if (isvalidkey)
    {
        printf("success\n%s\n", input);
    }
    else
    {
        printf("Usage: ./caesar key\n");
    }
}