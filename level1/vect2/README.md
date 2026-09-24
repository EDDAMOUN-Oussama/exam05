# vect2

## Goal

Implement a two-dimensional mathematical vector containing two integers.

The exercise is mainly about C++ operator overloading and const correctness.

## Files

~~~text
vect2.hpp   class implementation
vect2.cpp   translation unit required by the subject
main.cpp    local test program
subject.txt exercise statement
~~~

## Representation

~~~cpp
int x;
int y;
~~~

A vector such as:

~~~text
{2, 5}
~~~

is represented internally by x = 2 and y = 5.

## Main parts of the code

### Construction and assignment

The class supports:

- default construction as {0, 0};
- construction from two integers;
- copy construction;
- copy assignment.

### operator[]

There are two versions.

The const version returns a value:

~~~cpp
int operator[](int n) const;
~~~

The mutable version returns a reference:

~~~cpp
int& operator[](int n);
~~~

This is why both of these work:

~~~cpp
std::cout << v[1];
v[1] = 12;
~~~

No bounds checking is required by the subject.

### Addition and subtraction

~~~text
{1, 2} + {3, 4} -> {4, 6}
{5, 7} - {2, 3} -> {3, 4}
~~~

The class also implements += and -=.

### Scalar multiplication

Member multiplication handles:

~~~cpp
v * 3
~~~

because the vect2 object is on the left side.

The friend non-member overload handles:

~~~cpp
3 * v
~~~

because an int is on the left side.

That is the main reason both overloads are useful.

### Prefix and postfix operators

~~~text
++v  -> increment x and y, return the new vector
v++  -> keep the old vector, increment x and y, return the old vector

--v  -> decrement x and y, return the new vector
v--  -> keep the old vector, decrement x and y, return the old vector
~~~

### Unary minus

~~~text
-{2, -5} -> {-2, 5}
~~~

### Comparisons

Two vectors are equal only when both components are equal.

~~~cpp
x == other.x && y == other.y
~~~

### Stream output

The required format is:

~~~text
{x, y}
~~~

Example:

~~~text
{3, 6}
~~~

## Build

~~~bash
c++ -Wall -Wextra -Werror vect2.cpp main.cpp -o vect2_test
./vect2_test
~~~

Use the C++ standard required by the exam environment.

## What to remember for the exam

The most important ideas are:

- return references from compound assignment operators;
- distinguish prefix from postfix;
- provide const and non-const operator[];
- remember that v * n can be a member operator;
- remember that n * v needs a non-member/friend overload;
- keep operator<< const-correct.
