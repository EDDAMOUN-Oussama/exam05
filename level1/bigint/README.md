# bigint

## Goal

Implement an arbitrary-precision unsigned integer.

Native integer types have a fixed maximum size. This implementation stores the number as a decimal std::string, so arithmetic can continue beyond SIZE_MAX without losing precision.

## Files

~~~text
bigint.hpp   main implementation
bigint.cpp   translation unit required by the subject
main.cpp     local test program
subject.txt  exercise statement
~~~

The current implementation is mostly header-based.

## Internal representation

~~~cpp
std::string val;
~~~

Examples:

~~~text
0                    -> "0"
42                   -> "42"
18446744073709551616 -> "18446744073709551616"
~~~

Keeping the representation in decimal makes printing and decimal digit shifting straightforward.

## Main parts of the code

### Constructors and assignment

The class provides:

- default construction as 0;
- construction from size_t;
- copy construction;
- copy assignment.

### Stream output

operator<< sends the decimal string directly to the output stream.

~~~cpp
std::cout << value;
~~~

### Addition

Addition is performed manually from right to left.

For every position:

~~~text
sum   = left_digit + right_digit + carry
digit = sum % 10
carry = sum / 10
~~~

The result digits are produced in reverse order and then reversed once at the end.

This is the central arbitrary-precision part of the exercise.

### Increment

Prefix increment:

~~~cpp
++a
~~~

modifies the object and returns the updated object by reference.

Postfix increment:

~~~cpp
a++
~~~

stores a copy, increments the current object, and returns the old value.

### Comparisons

For unsigned decimal strings without leading zeros:

1. a number with more digits is larger;
2. if both lengths are equal, lexicographical string comparison gives the numeric order.

The implementation provides:

~~~text
==  !=  <  >  <=  >=
~~~

### Decimal digit shifts

These are decimal shifts, not binary bit shifts.

~~~text
42 << 3  -> 42000
1337 >> 2 -> 13
~~~

Left shift appends zero characters.

Right shift removes decimal digits from the end. If the requested shift is at least the number of digits, the value becomes 0.

## Complexity

For n decimal digits:

- comparison: O(n) in the equal-length case;
- addition: O(n);
- left shift by k: O(k) plus possible string reallocation;
- the current bigint-based right shift is intentionally simple rather than optimized.

## Build

~~~bash
c++ -Wall -Wextra -Werror bigint.cpp main.cpp -o bigint_test
./bigint_test
~~~

Use the C++ standard required by the exam environment.

## What to remember for the exam

The most important part to be able to rewrite is the addition loop:

~~~text
start from the last digit
while either number still has digits OR carry exists
    read missing digits as 0
    compute sum
    save sum % 10
    update carry with sum / 10
reverse the generated result
~~~

Also remember the semantic difference between:

~~~text
++a  -> increment, then return the new value
a++  -> save old value, increment, return the old value
~~~

and:

~~~text
a << n   -> returns a shifted copy
a <<= n  -> modifies a itself
~~~
