# vect2

> [!TIP]
> **Personal exam result: PASSED.**  
> I passed the `vect2` exercise in Exam Rank 05 using the implementation contained in this directory.

## Overview

`vect2` represents a two-dimensional mathematical vector containing two integers.

Although the exercise is small, it covers several fundamental C++ operator-overloading rules.

## Main concepts

- constructors and copy assignment;
- arithmetic operators;
- compound assignment;
- prefix/postfix increment and decrement;
- scalar multiplication;
- const and non-const `operator[]`;
- friend/non-member operators;
- stream output.

## Files

```text
vect2.hpp   Class implementation
vect2.cpp   Translation unit required by the subject
main.cpp    Local test program
subject.txt Exercise statement
```

## Representation

```cpp
int x;
int y;
```

Example:

```text
vect2(2, 5) -> {2, 5}
```

## Arithmetic operators

Vector arithmetic is component-wise:

```text
{1, 2} + {3, 4} -> {4, 6}
{5, 7} - {2, 3} -> {3, 4}
```

The implementation also supports:

```text
+=  -=  *=
```

## Scalar multiplication

Two forms are required:

```cpp
v * 3;
3 * v;
```

The member overload handles:

```cpp
v * 3
```

because the left operand is a `vect2`.

The friend/non-member overload handles:

```cpp
3 * v
```

because the left operand is an `int`.

This is one of the key ideas of the exercise.

## operator[]

Const access:

```cpp
int operator[](int n) const;
```

Mutable access:

```cpp
int &operator[](int n);
```

This allows both:

```cpp
std::cout << v[1];
v[1] = 12;
```

No bounds checking is required by the subject.

## Prefix vs postfix

```text
++v -> increment first, return the new value
v++ -> save old value, increment, return the old value

--v -> decrement first, return the new value
v-- -> save old value, decrement, return the old value
```

## Unary minus

```text
-{2, -5} -> {-2, 5}
```

## Equality

Two vectors are equal only when both coordinates are equal:

```cpp
x == other.x && y == other.y
```

## Output

Required format:

```text
{x, y}
```

Example:

```text
{3, 6}
```

## Build

```bash
c++ -Wall -Wextra -Werror vect2.cpp main.cpp -o vect2_test
./vect2_test
```

## Exam checklist

Make sure you can rewrite:

- const and non-const `operator[]`;
- prefix/postfix `++` and `--`;
- `v * n` versus `n * v`;
- `+=`, `-=`, `*=`;
- unary minus;
- `operator<<`;
- `==` and `!=`.

## Core idea

```text
member operator -> left operand is vect2
friend operator -> useful when the left operand is not vect2
```

## Personal note

This is the implementation style I used successfully during my Exam Rank 05 attempt.
