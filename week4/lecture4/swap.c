#include <stdio.h>

void swap(int x, int y);

int main(void)
{
    int x = 1;
    int y = 2;

    printf("x is %i\n", x);
    printf("y is %i\n", y);

    swap(x, y);

    printf("after swap, x is %i\n", x);
    printf("after y is %i\n", y);
}

void swap(int x, int y)
{
    int temp;
    temp = x;
    x = y;
    y = temp;
}