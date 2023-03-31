#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {

            float sum = image[i][j].rgbtGreen + image[i][j].rgbtRed + image[i][j].rgbtBlue;
            float avgofsum = sum / 3;
            int roundavg = round(avgofsum);

            image[i][j].rgbtGreen = roundavg;
            image[i][j].rgbtBlue = roundavg;
            image[i][j].rgbtRed = roundavg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int originalRed = image[i][j].rgbtRed;
            int originalGreen = image[i][j].rgbtGreen;
            int originalBlue = image[i][j].rgbtBlue;

            int sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            int sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            if (sepiaRed > 255)
                image[i][j].rgbtRed = 255;
            else
                image[i][j].rgbtRed = sepiaRed;

            if (sepiaGreen > 255)
                image[i][j].rgbtGreen = 255;
            else
                image[i][j].rgbtGreen = sepiaGreen;

            if (sepiaBlue > 255)
                image[i][j].rgbtBlue = 255;
            else
                image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
       for (int j = 0; j < width / 2; j++)
       {
           // Step 1: put RGB values of pixel on right side in temp variable

           int temp_red = image[i][width - j - 1].rgbtRed;
           int temp_green = image[i][width - j - 1].rgbtGreen;
           int temp_blue = image[i][width - j - 1].rgbtBlue;

           // Step 2: put RGB values of pixel on left side in pixel on right side

           image[i][width - j - 1].rgbtRed = image[i][j].rgbtRed;
           image[i][width - j - 1].rgbtGreen = image[i][j].rgbtGreen;
           image[i][width - j - 1].rgbtBlue = image[i][j].rgbtBlue;


            // Step 3: put RGB values in temp variable in pixel on left side

           image[i][j].rgbtRed = temp_red;
           image[i][j].rgbtGreen = temp_green;
           image[i][j].rgbtBlue = temp_blue;
       }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{

    RGBTRIPLE image_temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image_temp[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sum_red = 0;
            int sum_green = 0;
            int sum_blue = 0;
            float counter = 0.0;


            for (int h = -1; h < 2; h++)
            {
                for (int w = -1; w < 2; w++)
                {
                    if ((i + h < 0) || (i + h >= height) || (j + w < 0) || (j + w >= width))
                    {
                        continue;
                    }

                    sum_red += image_temp[i + h][j + w].rgbtRed;
                    sum_green += image_temp[i + h][j + w].rgbtGreen;
                    sum_blue += image_temp[i + h][j + w].rgbtBlue;
                    counter++;
                }
            }

            int avgRed = round(sum_red / counter);
            int avgGreen = round(sum_green / counter);
            int avgBlue = round(sum_blue / counter);

            image[i][j].rgbtRed = avgRed;
            image[i][j].rgbtGreen = avgGreen;
            image[i][j].rgbtBlue = avgBlue;

        }
    }
    return;
}