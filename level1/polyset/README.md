# polyset

## Goal

Extend the supplied bag hierarchy with searchable containers and then wrap a searchable bag in a set that prevents duplicate insertions.

This exercise is mainly about object-oriented C++ rather than algorithms.

## Directory structure

~~~text
polyset/
├── my_polyset/
│   ├── searchable_array_bag.hpp
│   ├── searchable_array_bag.cpp
│   ├── searchable_tree_bag.hpp
│   ├── searchable_tree_bag.cpp
│   ├── set.hpp
│   └── set.cpp
└── subject/
    ├── bag.hpp
    ├── searchable_bag.hpp
    ├── array_bag.hpp / .cpp
    ├── tree_bag.hpp / .cpp
    ├── main.cpp
    └── subject.en.txt
~~~

The files under subject are the supplied base code. The implementation written for the exercise is under my_polyset.

## Class relationships

Conceptually:

~~~text
             bag
            /   \
           /     \
  array_bag     searchable_bag
       \           /
        \         /
     searchable_array_bag
~~~

and:

~~~text
             bag
            /   \
           /     \
   tree_bag      searchable_bag
       \           /
        \         /
      searchable_tree_bag
~~~

array_bag, tree_bag, and searchable_bag use virtual inheritance from bag. This avoids having two independent bag subobjects in the derived searchable classes.

## searchable_array_bag

This class combines:

- the storage implementation of array_bag;
- the search interface of searchable_bag.

Its has() method performs a linear search through the protected data array.

~~~text
for every stored value
    if value == target
        return true
return false
~~~

## searchable_tree_bag

This class combines:

- the binary search tree implementation of tree_bag;
- the search interface of searchable_bag.

Its has() method follows the BST ordering:

~~~text
target == current -> found
target < current  -> go left
target > current  -> go right
~~~

This avoids traversing the whole tree in the normal case.

## set

A bag can contain duplicates. A set must keep unique values.

The set class wraps a searchable_bag and changes insertion behavior:

~~~text
if the value is not already present
    insert it
~~~

Other operations such as print(), clear(), and has() are delegated to the wrapped bag.

The current implementation stores the wrapped object as a reference:

~~~cpp
searchable_bag &bag;
~~~

so the set operates on the original searchable bag rather than owning a separate copy.

## Important C++ concepts

This exercise practices:

- abstract classes;
- pure virtual functions;
- polymorphism;
- multiple inheritance;
- virtual inheritance;
- protected members;
- const member functions;
- copy construction and assignment;
- composition/wrapping.

## Orthodox Canonical Form note

The subject explicitly asks for all written classes to follow Orthodox Canonical Form.

Before an exam submission, re-check that every required class has the exact constructors, copy constructor, assignment operator, and destructor expected by the subject.

In particular, the current set implementation should be reviewed carefully because it stores a reference member and currently does not define an assignment operator.

## Example build

From my_polyset:

~~~bash
c++ -Wall -Wextra -Werror \
    searchable_array_bag.cpp searchable_tree_bag.cpp set.cpp \
    ../subject/array_bag.cpp ../subject/tree_bag.cpp ../subject/main.cpp \
    -I. -I../subject -o polyset_test

./polyset_test 10 20 10 42
~~~

The exact standard/flags should match the exam environment.

## What to remember for the exam

Do not rewrite the supplied storage classes.

First inspect:

~~~text
bag
searchable_bag
array_bag
tree_bag
~~~

Then implement only the missing behavior.

The central idea is:

~~~text
existing storage + searchable interface = searchable bag
searchable bag + reject duplicates      = set
~~~
