// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>

#include "dictionary.h"

// Libraries that I added
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;


// Choose number of buckets in hash table
#define N 17576

const unsigned int chars_per_bucket = 3;

unsigned int num_of_words_in_dict = 0;

// Hash table
node *table[N];

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *dict = fopen(dictionary, "r");

    if (dict == NULL)
    {
        printf("Could not open dictionary.\n");
        return false;
    }

    // temporary string to store word from dictionary
    char tmp_word_from_dict[LENGTH + 1];

    // this loop goes through the dictionary, reading one string at a time
    while (fscanf(dict, "%s", tmp_word_from_dict) != EOF)
    {
        num_of_words_in_dict++;

        node *n = malloc(sizeof(node));

        if (n == NULL)
        {
            return false;
        }

        // copies the contents of the temporary string from the dictionary into n->word
        strcpy(n->word, tmp_word_from_dict);

        n->next = NULL;

        unsigned int hash_number;
        hash_number = hash(n->word);

        // This if statement translates to "if (there are already nodes at this hash location in the table)"
        if (table[hash_number] != NULL)
        {
            n->next = table[hash_number];
        }

        table[hash_number] = n;
    }

    fclose(dict);

    return true;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_number;
    hash_number = 0;

    char current_char;

    if (strlen(word) >= chars_per_bucket)
    {
        for (int i = 0; i < chars_per_bucket; i++)
        {
            current_char = tolower(word[i]);
            hash_number += (current_char - 'a') * ((int) pow(26, chars_per_bucket - i - 1));
        }
    }
    else
    {
        for (int i = 0; i < strlen(word); i++)
        {
            current_char = tolower(word[i]);
            hash_number = (current_char - 'a') * ((int) pow(26, strlen(word) - i - 1));
        }
    }

    return hash_number;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return num_of_words_in_dict;
}

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    unsigned int theoretical_hash_number;
    theoretical_hash_number = hash(word);

    for (node *tmp = table[theoretical_hash_number]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(tmp->word, word) == 0)
        {
            return true;
        }
    }

    return false;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            while (table[i] != NULL)
            {
                node *tmp = table[i]->next;
                free(table[i]);
                table[i] = tmp;
            }

        }
    }

    return true;
}