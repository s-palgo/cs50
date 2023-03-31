#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    FILE *file = fopen("filestuff.c", "a");
    if (file == NULL)
    {
        return 1;
    }

    char *name = "checking";

    fprintf(file, "%s\n", name);
}