#include <stdio.h>
#include <stdlib.h>

int square(int h, int w, int row, int col, char map[h][w + 1], char empty)
{
    int size = 0;
    while (row + size < h && col + size < w)
    {
        for (int i = 0; i <= size; i++)
            for (int j = 0; j <= size; j++)
                if (map[row + i][col + j] != empty)
                    return (size);
        size++;
    }
    return (size);
}

int err()
{
    fputs("Error: invalid map\n", stdout);
    return (1);
}

int bsq(FILE *f)
{
    char *line = NULL;
    size_t cap = 0;
    ssize_t len;
    int h = 0;

    len = getline(&line, &cap, f);
    if (len < 5 || line[len - 1] != '\n')
        return (err());
    char empty = line[len - 4];
    char obs = line[len - 3];
    char full = line[len -2];

    if (empty == obs || empty == full || obs == full
        || empty < 32 || empty > 126
        || obs < 32 || obs > 126
        || full < 32 || empty > 126)
        return (err());
    for (int i = 0; i < len - 4; i++)
    {
        if (line[i] < '0' || line[i] > '9')
            return (err());
        h = h * 10 + line[i] - '0';
    }
    if (h <= 0)
        return (err());
    
    len = getline(&line, &cap, f);
    if (len <= 1 || line[len - 1] != '\n')
        return (err());
    int w = len - 1;
    char map[h][len];

    for (int row = 0; row < h; row++)
    {
        if (row != 0)
            len = getline(&line, &cap, f);
        if (len != w + 1 || line[w] != '\n')
            return (err());
        for (int col = 0; col < w; col++)
        {
            if (line[col] != empty && line[col] != obs)
                return (err());
            map[row][col] = line[col];
        }
        map[row][w] = '\0';
    }

    if (getline(&line, &cap, f) != -1)
        return (err());
    int best = 0;
    int best_row = 0;
    int best_col = 0;

    for (int row = 0; row < h; row++)
    {
        for (int col = 0; col < w; col++)
        {
            int size = square(h, w, row, col, map, empty);
            if (size > best)
            {
                best = size;
                best_row = row;
                best_col = col;
            }
        }
    }

    for (int row = best_row; row < best_row + best; row++)
        for (int col = best_col; col < best_col + best; col++)
            map[row][col] = full;

    for (int row = 0; row < h; row++)
        printf("%s\n", map[row]);

    return (0);
}


int main(int ac, char **av)
{
    if (ac == 1)
        return (bsq(stdin));
    if (ac != 2)
        return (err());
    FILE *f = fopen(av[1], "r");
    if (!f) return (err());

    int res = bsq(f);
    fclose(f);
    return (res);
}














// #include <stdio.h>
// #include <stdlib.h>

// int square(int h, int w, char map[h][w + 1],
//            int row, int col, char empty)
// {
//     int size = 0;

//     while (row + size < h && col + size < w)
//     {
//         for (int i = 0; i <= size; i++)
//             for (int j = 0; j <= size; j++)
//                 if (map[row + i][col + j] != empty)
//                     return size;
//         size++;
//     }
//     return size;
// }

// int bsq(FILE *f)
// {
//     char    *line = NULL;
//     size_t  cap = 0;
//     ssize_t len;
//     int     h = 0;

//     /* ---------- HEADER ---------- */

//     len = getline(&line, &cap, f);

//     if (len < 5 || line[len - 1] != '\n')
//         return (fputs("Error: invalid map\n", stdout), 1);

//     char empty = line[len - 4];
//     char obstacle = line[len - 3];
//     char full = line[len - 2];

//     if (empty == obstacle || empty == full || obstacle == full
//         || empty < 32 || empty > 126
//         || obstacle < 32 || obstacle > 126
//         || full < 32 || full > 126)
//         return (fputs("Error: invalid map\n", stdout), 1);

//     for (int i = 0; i < len - 4; i++)
//     {
//         if (line[i] < '0' || line[i] > '9')
//             return (fputs("Error: invalid map\n", stdout), 1);

//         h = h * 10 + line[i] - '0';
//     }

//     if (h <= 0)
//         return (fputs("Error: invalid map\n", stdout), 1);


//     /* ---------- FIRST MAP LINE ---------- */

//     len = getline(&line, &cap, f);

//     if (len <= 1 || line[len - 1] != '\n')
//         return (fputs("Error: invalid map\n", stdout), 1);

//     int w = len - 1;

//     char map[h][w + 1];


//     /* ---------- READ MAP ---------- */

//     for (int row = 0; row < h; row++)
//     {
//         if (row != 0)
//         {
//             len = getline(&line, &cap, f);

//             if (len == -1)
//                 return (fputs("Error: invalid map\n", stdout), 1);
//         }

//         if (len != w + 1 || line[len - 1] != '\n')
//             return (fputs("Error: invalid map\n", stdout), 1);

//         for (int col = 0; col < w; col++)
//         {
//             if (line[col] != empty && line[col] != obstacle)
//                 return (fputs("Error: invalid map\n", stdout), 1);

//             map[row][col] = line[col];
//         }

//         map[row][w] = '\0';
//     }

//     /* Extra map lines are invalid */

//     if (getline(&line, &cap, f) != -1)
//         return (fputs("Error: invalid map\n", stdout), 1);


//     /* ---------- FIND BIGGEST SQUARE ---------- */

//     int best = 0;
//     int best_row = 0;
//     int best_col = 0;

//     for (int row = 0; row < h; row++)
//     {
//         for (int col = 0; col < w; col++)
//         {
//             int size = square(h, w, map, row, col, empty);

//             if (size > best)
//             {
//                 best = size;
//                 best_row = row;
//                 best_col = col;
//             }
//         }
//     }


//     /* ---------- FILL ---------- */

//     for (int row = best_row; row < best_row + best; row++)
//         for (int col = best_col; col < best_col + best; col++)
//             map[row][col] = full;


//     /* ---------- PRINT ---------- */

//     for (int row = 0; row < h; row++)
//         printf("%s\n", map[row]);

//     return 0;
// }

// int main(int ac, char **av)
// {
//     FILE *f;

//     if (ac == 1)
//         return bsq(stdin);

//     if (ac != 2)
//         return (fputs("Error: invalid arguments\n", stdout), 1);

//     f = fopen(av[1], "r");

//     if (!f)
//         return (fputs("Error: cannot open file\n", stdout), 1);

//     int ret = bsq(f);

//     fclose(f);

//     return ret;
// }
