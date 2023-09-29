#include "helpers.h"

void colorize(int height, int width, RGBTRIPLE image[height][width])
{
    // red rgb(228, 3, 3) #E40303
    // orange rgb(255, 140, 0) #FF8C00
    // yellow rgb(255, 237, 0) #FFED00
    // green rgb(0, 128, 38) #008026
    // indigo rgb(36, 64, 142) #24408E
    // violet rgb(115, 41, 130) #732982

    // red
    image[2][0].rgbtRed = 0xE4;
    image[2][0].rgbtGreen = 0x03;
    image[2][0].rgbtBlue = 0x03;

    image[2][7].rgbtRed = 0xE4;
    image[2][7].rgbtGreen = 0x03;
    image[2][7].rgbtBlue = 0x03;

    image[0][2].rgbtRed = 0xE4;
    image[0][2].rgbtGreen = 0x03;
    image[0][2].rgbtBlue = 0x03;

    image[7][2].rgbtRed = 0xE4;
    image[7][2].rgbtGreen = 0x03;
    image[7][2].rgbtBlue = 0x03;

    // orange
    image[3][0].rgbtRed = 0xff;
    image[3][0].rgbtGreen = 0x8C;
    image[3][0].rgbtBlue = 0x00;

    image[3][7].rgbtRed = 0xff;
    image[3][7].rgbtGreen = 0x8C;
    image[3][7].rgbtBlue = 0x00;

    image[0][3].rgbtRed = 0xff;
    image[0][3].rgbtGreen = 0x8C;
    image[0][3].rgbtBlue = 0x00;

    image[7][3].rgbtRed = 0xff;
    image[7][3].rgbtGreen = 0x8C;
    image[7][3].rgbtBlue = 0x00;

    // yellow
    image[4][0].rgbtRed = 0xff;
    image[4][0].rgbtGreen = 0xed;
    image[4][0].rgbtBlue = 0x00;

    image[4][7].rgbtRed = 0xff;
    image[4][7].rgbtGreen = 0xed;
    image[4][7].rgbtBlue = 0x00;

    image[0][4].rgbtRed = 0xff;
    image[0][4].rgbtGreen = 0xed;
    image[0][4].rgbtBlue = 0x00;

    image[7][4].rgbtRed = 0xff;
    image[7][4].rgbtGreen = 0xed;
    image[7][4].rgbtBlue = 0x00;

    // green
    image[5][0].rgbtRed = 0x00;
    image[5][0].rgbtGreen = 0x80;
    image[5][0].rgbtBlue = 0x26;

    image[5][7].rgbtRed = 0x00;
    image[5][7].rgbtGreen = 0x80;
    image[5][7].rgbtBlue = 0x26;

    image[0][5].rgbtRed = 0x00;
    image[0][5].rgbtGreen = 0x80;
    image[0][5].rgbtBlue = 0x26;

    image[7][5].rgbtRed = 0x00;
    image[7][5].rgbtGreen = 0x80;
    image[7][5].rgbtBlue = 0x26;

    // indigo
    image[1][1].rgbtRed = 0x24;
    image[1][1].rgbtGreen = 0x40;
    image[1][1].rgbtBlue = 0x8e;

    image[1][6].rgbtRed = 0x24;
    image[1][6].rgbtGreen = 0x40;
    image[1][6].rgbtBlue = 0x8e;

    image[6][1].rgbtRed = 0x24;
    image[6][1].rgbtGreen = 0x40;
    image[6][1].rgbtBlue = 0x8e;

    image[6][6].rgbtRed = 0x24;
    image[6][6].rgbtGreen = 0x40;
    image[6][6].rgbtBlue = 0x8e;

    // violet
    image[2][2].rgbtRed = 0x73;
    image[2][2].rgbtGreen = 0x29;
    image[2][2].rgbtBlue = 0x82;

    image[2][5].rgbtRed = 0x73;
    image[2][5].rgbtGreen = 0x29;
    image[2][5].rgbtBlue = 0x82;

    image[4][2].rgbtRed = 0x73;
    image[4][2].rgbtGreen = 0x29;
    image[4][2].rgbtBlue = 0x82;

    image[4][5].rgbtRed = 0x73;
    image[4][5].rgbtGreen = 0x29;
    image[4][5].rgbtBlue = 0x82;

    image[5][3].rgbtRed = 0x73;
    image[5][3].rgbtGreen = 0x29;
    image[5][3].rgbtBlue = 0x82;

    image[5][4].rgbtRed = 0x73;
    image[5][4].rgbtGreen = 0x29;
    image[5][4].rgbtBlue = 0x82;
}
