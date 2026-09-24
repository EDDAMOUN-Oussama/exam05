# BSQ

## Goal

Find the biggest square made only of empty cells while avoiding obstacles, fill it with the full character, and print the updated map.

This repository uses an intentionally simple exhaustive-search solution rather than Dynamic Programming.

## Files

~~~text
my_bsq.c     current implementation
exmple       sample map
test.py      original/reference tester used during preparation
test_bsq.py  expanded tester added for this repository
~~~

## Input format

The first line contains:

~~~text
<number_of_rows><empty><obstacle><full>\n
~~~

Example:

~~~text
9.ox
~~~

means:

~~~text
height   = 9
empty    = '.'
obstacle = 'o'
full     = 'x'
~~~

The three map characters may be any printable characters, including digits.

That is why the implementation reads the complete header with getline() and takes the last three characters before the newline as the map symbols.

Everything before them must represent the height.

## Valid map requirements

The subject requires:

- at least one row;
- at least one cell per row;
- exactly the declared number of rows;
- every map row has the same width;
- every map row ends with a newline;
- map cells contain only empty or obstacle;
- empty, obstacle, and full are all distinct;
- the header contains exactly the height followed by the three symbols;
- the three symbols are printable.

Invalid maps must print:

~~~text
Error: invalid map
~~~

followed by a newline.

Other failures should start with:

~~~text
Error:
~~~

and contain a meaningful message.

## Reading the map

The first map row determines the width:

~~~c
width = line_length - 1;
~~~

The minus one removes the newline.

A variable-length array is then used:

~~~c
char map[height][width + 1];
~~~

The extra column stores the terminating '\0' so each row can be printed as a C string.

Every following row is checked against the same width.

## Square search — without Dynamic Programming

For every possible starting position:

~~~text
(row, col)
~~~

the square() function tries progressively larger squares.

Conceptually:

~~~text
1x1
2x2
3x3
...
~~~

The search stops when:

- the square reaches the map boundary; or
- any cell inside the candidate square is not the empty character.

The returned value is the largest valid side length starting at that position.

### Why the boundary check matters

The loop checks:

~~~c
row + size < height
col + size < width
~~~

Without this, an all-empty map could make the search read outside the array.

## Choosing the correct square

The map is scanned:

~~~text
top to bottom
left to right
~~~

The best result is updated only when:

~~~c
size > best
~~~

and not when size == best.

This naturally implements the subject's tie-breaking rule:

1. choose the topmost square;
2. if several are equally high, choose the leftmost one.

## Filling the result

Once the best top-left position and side length are known, two loops replace all cells in that square with the full character.

## Complexity

This solution is intentionally simple, not optimal.

Because candidate squares repeatedly scan cells that may already have been checked, the worst-case running time is much higher than the classic Dynamic Programming solution.

The advantage is that the algorithm is straightforward to understand and rewrite under exam pressure.

A Dynamic Programming solution can solve the search in O(height * width), while this brute-force approach trades performance for simplicity.

## Build

~~~bash
cc -Wall -Wextra -Werror my_bsq.c -o bsq
~~~

## Run

With a file:

~~~bash
./bsq exmple
~~~

From standard input:

~~~bash
cat exmple | ./bsq
~~~

## Testing

Run the expanded tester with:

~~~bash
python3 test_bsq.py ./bsq
~~~

The tester checks both file input and stdin and includes:

- subject-style examples;
- all-empty maps;
- all-obstacle maps;
- single-row and single-column maps;
- tie-breaking;
- unusual printable characters;
- numeric map symbols;
- invalid headers;
- wrong row counts;
- inconsistent widths;
- invalid map characters;
- missing final newlines;
- extra map rows;
- randomized valid maps checked against an independent reference solver.

## Important note about the current implementation

Before using the current my_bsq.c as a final exam submission, compare its exact error messages with the subject.

The subject requires:

~~~text
Error: invalid map
~~~

while the current source prints:

~~~text
Error: Invalid map
~~~

The capital I is different and strict output tests may reject it.

Also remember that this VLA-based implementation stores the map on the stack. It is deliberately simple, but a malloc-based implementation is more robust for very large maps.

## What to remember for the exam

The complete idea is:

~~~text
read and validate header
-> read first row and discover width
-> read exactly height rows
-> validate every row and character
-> reject extra rows
-> test a square from every cell
-> keep only a strictly bigger result
-> fill the best square
-> print the map
~~~

The core non-DP idea is simply:

~~~text
from every cell, grow a square until it becomes invalid
~~~
