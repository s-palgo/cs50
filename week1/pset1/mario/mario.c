#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // ask user for height
    int height;
    do
    {
        height = get_int("Height (between 1 and 8 inclusive): \n");
    }
    while (height < 1 || height > 8);

    // create a pyramid
    for (int line = 0; line < height; line++)
    {
        for (int j = 0; j < height - line - 1; j++)
        {
            printf(" ");
        }
        for (int k = 0; k < line + 1; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}