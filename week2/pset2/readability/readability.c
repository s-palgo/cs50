#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

//Prototypes
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Ask user for text
    string text = get_string("Text: ");

    // Calculate number of letters in text
    int letters = count_letters(text);
    // Calculate number of words in text
    int words = count_words(text);
    // Calculate number of sentences in text
    int sentences = count_sentences(text);

    // Calculate average number of letters per 100 words
    float L = (100 * letters) / (float) words;
    // Calculate average number of sentences per 100 words
    float S = (100 * sentences) / (float) words;
    // Coleman-Liau reading level index
    float index = (float)(0.0588 * L - 0.296 * S - 15.8);
    // Round Coleman-Liau index to nearest integer
    int reading_level = round(index);

    // Print reading level on screen
    if (index < 1)
    {
        printf("Before Grade 1");
        printf("\n");
    }
    if (index >= 1 && index < 16)
    {
        printf("Grade %i\n", reading_level);
    }
    if (index >= 16)
    {
        printf("Grade 16+");
        printf("\n");
    }
}

// Calculate number of letters in text
int count_letters(string text)
{
    int counter_letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            counter_letters++;
        }
    }
    return counter_letters;
}

// Calculate number of words in text
int count_words(string text)
{
    int counter_words = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            counter_words++;
        }
    }
    counter_words += 1;
    return counter_words;
}

// Calculate number of sentences in text
int count_sentences(string text)
{
    int counter_sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            counter_sentences++;
        }
    }
    return counter_sentences;
}