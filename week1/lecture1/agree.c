#include <cs50.h>
#include <stdio.h>

int main(void)
{
    char c = get_char("Do you agree? ");
    if (c == 'y' || c == 'Y')
    {
        printf("You're in! \n");
    }
    else if (c == 'n' || c == 'N')
    {
        printf("Sorry, we can't let you in :( \n");
    }
}