#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    int count = 0;
    for (int i = 0; i < height; ++i)
    {
        count = 0;
        for (int j = i + 1; j < height; ++j)
        {
            printf(" ");
        }

        while (count <= i)
        {
            printf("#");
            count++;
        }

        printf("\n");
    }
}