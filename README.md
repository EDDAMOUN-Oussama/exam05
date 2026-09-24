# 42 Exam Rank 05 — Preparation Repository

Personal preparation repository for **42 Exam Rank 05**, organized by exam level and focused on understanding, rewriting, and testing each exercise under exam conditions.

> [!IMPORTANT]
> This is a personal study repository, not an official 42 repository. The subject provided during the exam is always the final reference.

## Progress

| Level | Exercise | Language | Main focus | Personal status |
|---|---|---|---|---|
| 1 | [bigint](level1/bigint/) | C++ | Arbitrary precision, operators, string arithmetic | Practice |
| 1 | [vect2](level1/vect2/) | C++ | Operator overloading, const correctness | ✅ **Passed with this implementation** |
| 1 | [polyset](level1/polyset/) | C++ | Polymorphism, virtual inheritance, wrappers | Practice |
| 2 | [life](level2/life/) | C | Game of Life, double buffering | Practice |
| 2 | [BSQ](level2/BSQ/) | C | Parsing, validation, largest-square search | ✅ **Passed with this implementation approach** |

## Repository structure

```text
exam05/
├── level1/
│   ├── bigint/
│   ├── vect2/
│   └── polyset/
└── level2/
    ├── life/
    └── BSQ/
```

Each exercise directory contains its own README with the objective, implementation idea, important code concepts, compilation examples, edge cases, and exam notes.

## Exercise overview

### Level 1

#### bigint
Implements an unsigned arbitrary-precision integer using a decimal string.

Main topics:
- manual addition with carry;
- comparisons;
- prefix/postfix increment;
- decimal digit shifts;
- stream output;
- operator overloading.

#### vect2
Implements a 2D integer vector and practices C++ operator overloading.

Main topics:
- arithmetic and compound operators;
- scalar multiplication in both directions;
- prefix/postfix `++` and `--`;
- const/non-const `operator[]`;
- unary minus;
- equality;
- stream output.

> [!NOTE]
> I personally passed **vect2** in Exam Rank 05 using the implementation contained in this repository.

#### polyset
Extends the supplied bag hierarchy with searchable implementations and a set wrapper.

Main topics:
- abstract classes;
- polymorphism;
- multiple/virtual inheritance;
- const correctness;
- wrapper design.

### Level 2

#### life
Simulates Conway's Game of Life after drawing generation 0 from commands read on standard input.

Main topics:
- command parsing;
- padded grids;
- neighbor counting;
- double buffering;
- exact output formatting.

#### BSQ
Finds the biggest square of empty cells while avoiding obstacles.

This repository intentionally uses a **non-Dynamic-Programming brute-force approach** because it is simple to understand and rewrite under exam conditions.

> [!NOTE]
> I personally passed **BSQ** in Exam Rank 05 using this implementation approach.

An extended tester is included at:

```text
level2/BSQ/test_bsq.py
```

## Preparation workflow

```text
read the subject
      ↓
understand the required behavior
      ↓
rewrite the solution without looking
      ↓
compile with strict warnings
      ↓
test edge cases
      ↓
compare again with the subject
```

My preparation order was:

```text
bigint -> life -> polyset -> vect2 -> BSQ
```

## Compilation

Typical examples:

```bash
# C
cc -Wall -Wextra -Werror file.c -o program

# C++
c++ -Wall -Wextra -Werror file.cpp main.cpp -o program
```

Always follow the compiler and language standard required by the actual exam subject.

## Acknowledgements

Special thanks to:

- [aychikhi/42-Exam05](https://github.com/aychikhi/42-Exam05) — very helpful for understanding and practicing the Level 1 exercises and **Life**.
- [Prometheus1994/42-Exam-Rank-05-Without-dynamic-programming](https://github.com/Prometheus1994/42-Exam-Rank-05-Without-dynamic-programming) — gave me the idea of approaching **BSQ without Dynamic Programming**.
- [Redadaghouj/Exam-Rank-05](https://github.com/Redadaghouj/Exam-Rank-05) — provided a useful BSQ testing base. I reviewed it and added a stricter expanded tester in this repository.

Thanks to the authors for sharing their work with the 42 community.

## Disclaimer

These solutions are published for learning and exam preparation. Subjects may change, so always read the exercise statement you receive before reusing an implementation.
