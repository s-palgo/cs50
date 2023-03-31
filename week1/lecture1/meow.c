#include <cs50.h>
#include <stdio.h>

// Prototype
void meow(int n);

int main(void)
{
    // for (int i = 0; i < 5; i++)
    //{
        meow(5);
    //}
}

void meow(int n)
{
    for (int i = 0; i < n; i++)
    {
        printf("meow\n");
    }
}