# life

## Goal

Simulate Conway's Game of Life after drawing the initial generation with commands received from standard input.

The program is called as:

~~~bash
./life width height iterations
~~~

The board is drawn first, then the requested number of Game of Life generations is simulated.

## Files

~~~text
life.c       implementation
subject.txt  exercise statement
~~~

## Input commands

A virtual pen starts in the top-left cell.

The commands are:

~~~text
w -> move up
a -> move left
s -> move down
d -> move right
x -> toggle the pen up/down
~~~

The pen starts up, so movement initially does not draw anything.

When the pen is down, the current cell becomes alive after each command.

Commands that would move outside the board leave the pen in the same position.

Unknown commands do nothing.

## Board representation

The implementation uses:

~~~c
int grid[2][height + 2][width + 2];
~~~

There are two important ideas here.

### 1. Two generations

~~~text
grid[0] -> one generation
grid[1] -> the other generation
~~~

During iteration i:

~~~text
current = grid[i % 2]
next    = grid[(i + 1) % 2]
~~~

This avoids modifying the current generation while it is still being used to calculate neighboring cells.

After all iterations, the final generation is:

~~~text
grid[iterations % 2]
~~~

### 2. Dead border

The real board occupies:

~~~text
rows    1 .. height
columns 1 .. width
~~~

The extra border around it stays zero.

Because cells outside the board are considered dead, this lets the code count all eight neighbors without writing separate edge/corner conditions.

## Drawing generation 0

The initial pen position is:

~~~text
row = 1
column = 1
pen = up
~~~

The command loop updates the position or toggles the pen.

When the pen is down:

~~~c
grid[0][x][y] = 1;
~~~

The drawing always goes into grid[0] because this is generation 0, before simulation starts.

## Game of Life rules

For every cell, the code counts its eight neighbors.

The rules are:

~~~text
live cell with fewer than 2 neighbors -> dies
live cell with 2 or 3 neighbors       -> survives
live cell with more than 3 neighbors  -> dies
dead cell with exactly 3 neighbors    -> becomes alive
~~~

The implementation reduces this to:

~~~c
if ((nb == 2 && alive) || nb == 3)
    next = 1;
else
    next = 0;
~~~

A useful way to remember it is:

~~~text
3 neighbors -> alive
2 neighbors -> alive only if already alive
everything else -> dead
~~~

## Neighbor counting

The code scans offsets from -1 to 1 in both dimensions:

~~~text
(-1,-1) (-1,0) (-1,1)
( 0,-1)  cell   ( 0,1)
( 1,-1) ( 1,0) ( 1,1)
~~~

Only the center offset (0,0) is skipped.

## Output

Alive cells are printed as:

~~~text
O
~~~

Dead cells are printed as spaces.

Every board row ends with a newline.

For debugging exact spaces, cat -e is useful:

~~~bash
echo 'dxss' | ./life 3 3 1 | cat -e
~~~

Expected shape:

~~~text
   $
OOO$
   $
~~~

## Build

~~~bash
cc -Wall -Wextra -Werror life.c -o life
~~~

## Useful tests

No simulation:

~~~bash
echo 'dxss' | ./life 3 3 0
~~~

One iteration of the blinker:

~~~bash
echo 'dxss' | ./life 3 3 1
~~~

Two iterations:

~~~bash
echo 'dxss' | ./life 3 3 2
~~~

This pattern is especially useful because it verifies the double-buffer logic:

~~~text
vertical -> horizontal -> vertical
~~~

## What to remember for the exam

The essential structure is:

~~~text
parse width / height / iterations
-> initialize two padded grids
-> read drawing commands into grid[0]
-> for each generation:
       count 8 neighbors
       write only into the other grid
-> print grid[iterations % 2]
~~~

The two details most likely to cause mistakes are:

- using the wrong movement boundary, especially d with y < width;
- writing the next generation into the same grid currently being read.
