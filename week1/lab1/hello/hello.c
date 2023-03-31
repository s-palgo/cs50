#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Ask user for name
    string name = get_string("What is your name? \n");
    // Print "hello, 'name'" using the name submitted by user
    printf("hello, %s", name);
}