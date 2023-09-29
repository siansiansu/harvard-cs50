// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 65536;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    char lowercase_word[LENGTH + 1];
    for (int i = 0; i < strlen(word); i++)
    {
        lowercase_word[i] = tolower(word[i]);
    }

    node *cursor = table[hash(lowercase_word)];

    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Improve this hash function
    // This hash function is inspired by these two articles.
    // ref: https://www.digitalocean.com/community/tutorials/hash-table-in-c-plus-plus
    // ref: https://stackoverflow.com/questions/7666509/hash-function-for-string
    // return toupper(word[0]) - 'A';
    unsigned long hash = 0;
    // for (int i = 0; i < strlen(word); i++)
    hash += toupper(word[0]);
    hash += (hash << 10);
    hash ^= (hash >> 6);
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *infile = fopen(dictionary, "r");
    if (!infile)
    {
        printf("Error opening file!\n");
        return false;
    }
    char next_word[LENGTH + 1];
    while (fscanf(infile, "%s", next_word) != EOF)
    {
        node *new = malloc(sizeof(node));
        if (new == NULL)
        {
            unload();
            return false;
        }
        strcpy(new->word, next_word);
        int hash_value = hash(next_word);
        new->next = table[hash_value];
        table[hash_value] = new;
    }
    fclose(infile);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int word_count = 0;
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            word_count++;
            cursor = cursor->next;
        }
    }
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
        free(cursor);
    }
    return true;
}