#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    const int BLOCK_SIZE = 512;
    if (argc < 2)
    {
        printf("Usage: ./recover [file.raw]\n");
        return 1;
    }

    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s\n", argv[1]);
        return 1;
    }

    unsigned char buffer[BLOCK_SIZE];
    int counter = 0;
    FILE *img = NULL;
    while (fread(buffer, sizeof(unsigned char), BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            if (img != NULL)
            {
                fclose(img);
            }
            char filename[8];
            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");
            if (img == NULL)
            {
                fclose(img);
                fprintf(stderr, "Could not create %s\n", filename);
                return 1;
            }
            counter++;
        }
        if (img != NULL)
        {
            fwrite(buffer, sizeof(unsigned char), BLOCK_SIZE, img);
        }
    }
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(file);
}