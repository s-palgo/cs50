#include <cs50.h>
#include <stdio.h>

int get_positive_int(void);

int main(void)
{
    int i = get_positive_int();
}

int get_positive_int(void)
{
    int n;
    do
    {
        n = get_int("Positive integer: ");
    }
    while (n < 1);
    return n;
}