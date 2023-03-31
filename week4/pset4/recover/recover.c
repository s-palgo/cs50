#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // return error message if user doesn't type in correct # of arguments
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw\n");
        return 1;
    }

    // check if card.raw can be opened
    // if it can, open it
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 2;
    }

    // creates an 8-character array to store file name
    // (7 character for name + nul character)
    char filename[8];

    // this integer counter will keep track of # of jpegs found
    int jpegcount = 0;

    // this boolean will check if jpeg has been found
    // once a jpeg is found, the value of this boolean will be true
    bool jpegfound = false;


    // a pointer to an image file which we'll write our individual bytes to
    FILE *img = NULL;

    // a buffer of 512 bytes that will be read and processed
    BYTE bytes[512];


    // looping through each 512-byte buffer
    while (fread(bytes, sizeof(BYTE), 512, input))
    {
        // this is to check whether we've found a jpeg header or not
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff &&
            (bytes[3] & 0xf0) == 0xe0)
        {
            // this condition checks whether we're on our first jpeg
            // if this condition evaluates to true, we're NOT on our first jpeg
            if (jpegcount != 0)
            {
                fclose(img);
            }


            jpegfound = true;

            // update jpegcount after a jpeg is found
            jpegcount++;

            // create jpeg name based on which jpeg in the forensic image it is
            sprintf(filename, "%03i.jpg", jpegcount - 1);


            // open image file for writing bytes to it
            img = fopen(filename, "w");
            fwrite(bytes, sizeof(BYTE), 512, img);
        }


        // this runs if jpeg header has not been found
        else
        {
            if (jpegfound)
            {
                fwrite(bytes, sizeof(BYTE), 512, img);
            }
        }
    }

    // close all open files
    fclose(input);
    fclose(img);
}