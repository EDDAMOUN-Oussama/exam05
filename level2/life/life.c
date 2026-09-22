#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int ac, char **av)
{
    if (ac != 4)
        return (1);
    int width = atoi(av[1]);
    int height = atoi(av[2]);
    int its = atoi(av[3]);

    if (width <= 0 || height <= 0 || its < 0)
        return (1);

    int grid[2][height + 2][width + 2];

    for (int it = 0; it < 2; it++)
        for (int h = 0; h < height + 2; h++)
            for (int w = 0; w < width + 2; w++) grid[it][h][w] = 0;
    
    int x = 1, y = 1, pen = 0;
    char cmd;

    while (read(0, &cmd, 1) > 0)
    {
        if (cmd == 'x') pen = !pen;
        else if (cmd == 'w' && x > 1) x--;
        else if (cmd == 'a' && y > 1) y--;
        else if (cmd == 's' && x < height) x++;
        else if (cmd == 'd' && y < width) y++;
        if (pen) grid[0][x][y] = 1;
    }

    for (int it = 0; it < its; it++)
        for (int h = 1; h <= height; h++)
            for (int w = 1; w <= width; w++)
            {
                int nb = 0;
                for (int x = -1; x <= 1; x++)
                    for (int y = -1; y <= 1; y++)
                        if (!(x == 0 && y == 0)) nb += grid[it % 2][h + x][w + y];
                if ((nb == 2 && grid[it % 2][h][w]) || nb == 3) grid[(it + 1) % 2][h][w] = 1;
                else grid[(it + 1) % 2][h][w] = 0;
            }

    for (int h = 1; h <= height; h++)
    {
        for (int w = 1; w <= width; w++) putchar(grid[its % 2][h][w]? 'O': ' ');
        putchar ('\n');
    }
    return (0);
}
