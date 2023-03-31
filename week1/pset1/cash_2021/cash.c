#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollars;
    do
    {
        dollars = get_float("Change in dollars: ");
    }
    while (dollars < 0.00);

    int cents;
    {
        cents = round(dollars * 100);
    }

    int counter = 0;
    while (cents > 24)
    {
        cents = cents - 25;
        counter++;
    }
    while (cents > 9)
    {
        cents = cents - 10;
        counter++;
    }
    while (cents > 4)
    {
        cents = cents - 5;
        counter++;
    }
    while (cents > 0)
    {
        cents = cents - 1;
        counter++;
    }
    printf("%i\n", counter);
}