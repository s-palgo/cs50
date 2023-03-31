#include <cs50.h>
#include <stdio.h>

void valid_triangle(int a, int b, int c);

int main(void)
{
    // Ask user for three triangle lengths

    int x = get_int("Side 1: ");
    int y = get_int("Side 2: ");
    int z = get_int("Side 3: ");

    valid_triangle(x, y, z);
    printf("\n");
}

void valid_triangle(int a, int b, int c)
{
    if ((a > 0) && (b > 0) && (c > 0) && (a + b > c) && (b + c > a) && (a + c > b))
    {
        printf("true");
    }
    else {
        printf("false");
    }
}