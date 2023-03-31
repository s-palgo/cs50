#include <cs50.h>
#include <stdio.h>

void meow();
int main(void)
{
    long x = get_int("x: ");

    long y = get_int("y: ");

    printf("%li\n", x + y);
    
    int n = 5;
    
    meow(n);
}

void meow(int n)
{
    
    for (int j = 0; j < n; j++)
    {
        printf("meow\n");
    }
}