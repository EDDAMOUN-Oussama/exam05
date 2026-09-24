# 42 Exam Rank 05 — Practice Repository

This repository contains my personal preparation work for the current 42 Exam Rank 05 exercises.

> This is a study repository, not an official 42 repository. Subjects and exam details can change, so the subject provided during the exam is always the final reference.

## Repository structure

~~~text
exam05/
├── level1/
│   ├── bigint/
│   ├── vect2/
│   └── polyset/
└── level2/
    ├── life/
    └── BSQ/
~~~

## Exercises

| Level | Exercise | Language | Main topics |
|---|---|---|---|
| 1 | bigint | C++ | arbitrary precision integers, operator overloading, string arithmetic |
| 1 | vect2 | C++ | 2D vectors, operator overloading, const/non-const access |
| 1 | polyset | C++ | abstract classes, polymorphism, virtual/multiple inheritance, wrappers |
| 2 | life | C | Game of Life, input commands, double buffering, neighbor counting |
| 2 | BSQ | C | parsing, map validation, exhaustive square search, tie-breaking |

Each exercise directory contains a dedicated README explaining the idea, the code structure, important operators/functions, how to compile it, and exam notes.

## Level 1

### bigint

The bigint class stores an unsigned integer as a decimal string so it can represent values larger than the native integer types.

The current implementation covers:

- construction and copying;
- stream output;
- arbitrary-length addition;
- +=;
- prefix and postfix ++;
- all comparison operators;
- decimal left shift;
- decimal right shift.

The key idea is manual arithmetic on decimal digits using carry propagation.

See: level1/bigint/README.md

### vect2

The vect2 class represents a two-dimensional integer vector.

The implementation practices:

- arithmetic operators;
- scalar multiplication in both directions;
- prefix/postfix increment and decrement;
- mutable and const operator[];
- unary minus;
- equality and inequality;
- stream output.

See: level1/vect2/README.md

### polyset

polyset is mainly an object-oriented design exercise.

It combines the supplied bag hierarchy with:

- searchable_array_bag;
- searchable_tree_bag;
- set.

The exercise is useful for understanding abstract interfaces, polymorphism, multiple inheritance, virtual inheritance, const correctness, and the difference between a bag and a set.

See: level1/polyset/README.md

## Level 2

### life

The Life solution:

1. reads drawing commands from stdin;
2. builds generation 0;
3. uses a padded board so outside cells behave as dead cells;
4. alternates between two grids;
5. counts the eight neighbors of each cell;
6. applies Conway's Game of Life rules;
7. prints the requested generation.

See: level2/life/README.md

### BSQ

The BSQ solution in this repository intentionally uses an exhaustive search approach instead of Dynamic Programming.

It:

1. parses the header;
2. validates the map;
3. stores the map in a variable-length array;
4. tries the largest possible square from every position;
5. keeps the first largest square found;
6. fills that square with the full character;
7. prints the final map.

Because positions are scanned from top to bottom and left to right, and the best square is updated only for a strictly larger size, ties naturally keep the topmost and then leftmost solution.

A stronger tester is included as:

~~~text
level2/BSQ/test_bsq.py
~~~

See: level2/BSQ/README.md

## Suggested preparation order

The order I used while preparing is:

~~~text
bigint -> life -> polyset -> vect2 -> BSQ
~~~

The exercises test different skills, so the goal is not only to memorize code but to be able to rebuild each solution from its core idea.

## General compilation notes

Use the compiler and standard required by the subject/exam environment.

Typical examples:

~~~bash
# C
cc -Wall -Wextra -Werror file.c -o program

# C++
c++ -Wall -Wextra -Werror file.cpp main.cpp -o program
~~~

For polyset, the supplied subject classes must also be compiled and their include directory added.

## Acknowledgements

A big thank you to the following repositories that helped me during preparation:

- [aychikhi/42-Exam05](https://github.com/aychikhi/42-Exam05) — very helpful for understanding and practicing the Level 1 exercises and Life.
- [Prometheus1994/42-Exam-Rank-05-Without-dynamic-programming](https://github.com/Prometheus1994/42-Exam-Rank-05-Without-dynamic-programming) — gave me the idea of solving BSQ without Dynamic Programming.
- [Redadaghouj/Exam-Rank-05](https://github.com/Redadaghouj/Exam-Rank-05) — provided the base idea for the BSQ testing workflow. I reviewed that tester and created an expanded version in this repository.

Thanks to the authors for sharing their work with the 42 community.

## Final note

The most useful way to use this repository is:

~~~text
read the subject
-> understand the idea
-> rewrite the solution without looking
-> compile with strict warnings
-> test edge cases
-> compare the result with the subject
~~~

Good luck with Exam Rank 05.
