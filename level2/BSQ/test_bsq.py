#!/usr/bin/env python3
"""
Extended tester for the 42 Exam Rank 05 BSQ exercise.

Usage:
    python3 test_bsq.py ./bsq

The reference parser follows the subject used in this repository:
- header = decimal row count + exactly 3 printable characters
- the last 3 header characters are empty / obstacle / full
- this correctly supports digit characters as map symbols
- every map line, including the last one, must end with '\n'
- exactly the declared number of map rows must exist
"""

import os
import random
import subprocess
import sys
import tempfile

ERROR = "Error: invalid map\n"

GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


def parse_reference(content):
    if not content:
        return None
    if not content.endswith("\n"):
        return None

    lines = content.splitlines(keepends=True)
    if not lines:
        return None

    header = lines[0]
    if not header.endswith("\n"):
        return None
    raw = header[:-1]

    # At least one digit for height + exactly 3 symbols.
    if len(raw) < 4:
        return None

    height_part = raw[:-3]
    empty, obstacle, full = raw[-3:]

    if not height_part or not height_part.isdigit():
        return None

    height = int(height_part)
    if height <= 0:
        return None

    for c in (empty, obstacle, full):
        if not (32 <= ord(c) <= 126):
            return None
    if len({empty, obstacle, full}) != 3:
        return None

    # Exactly height map rows and no extra rows.
    if len(lines) != height + 1:
        return None

    rows = []
    width = None

    for raw_row in lines[1:]:
        if not raw_row.endswith("\n"):
            return None
        row = raw_row[:-1]

        if width is None:
            width = len(row)
            if width == 0:
                return None
        elif len(row) != width:
            return None

        if any(c != empty and c != obstacle for c in row):
            return None

        rows.append(list(row))

    return height, width, empty, obstacle, full, rows


def solve_reference(content):
    parsed = parse_reference(content)
    if parsed is None:
        return ERROR

    height, width, empty, obstacle, full, grid = parsed

    # A DP solver is used only as an independent oracle for testing.
    dp = [[0] * width for _ in range(height)]
    best_size = 0
    best_row = 0
    best_col = 0

    for r in range(height):
        for c in range(width):
            if grid[r][c] == obstacle:
                dp[r][c] = 0
            elif r == 0 or c == 0:
                dp[r][c] = 1
            else:
                dp[r][c] = 1 + min(
                    dp[r - 1][c],
                    dp[r][c - 1],
                    dp[r - 1][c - 1],
                )

            size = dp[r][c]
            if size:
                top = r - size + 1
                left = c - size + 1
                if (
                    size > best_size
                    or (
                        size == best_size
                        and (top < best_row or (top == best_row and left < best_col))
                    )
                ):
                    best_size = size
                    best_row = top
                    best_col = left

    for r in range(best_row, best_row + best_size):
        for c in range(best_col, best_col + best_size):
            grid[r][c] = full

    return "".join("".join(row) + "\n" for row in grid)


def run(binary, content=None, as_file=False, args=None, timeout=3.0):
    args = args or []

    try:
        if as_file:
            fd, path = tempfile.mkstemp(prefix="bsq_", suffix=".map", text=True)
            try:
                with os.fdopen(fd, "w") as f:
                    f.write(content)
                p = subprocess.run(
                    [binary, path] + args,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
            finally:
                try:
                    os.unlink(path)
                except FileNotFoundError:
                    pass
        else:
            p = subprocess.run(
                [binary] + args,
                input=content or "",
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        return p.stdout, p.stderr, p.returncode, None
    except subprocess.TimeoutExpired:
        return "", "", None, "TIMEOUT"


def valid_cases():
    return [
        (
            "subject example",
            "9.ox\n"
            "...........................\n"
            "....o......................\n"
            "............o..............\n"
            "...........................\n"
            "....o......................\n"
            "...............o...........\n"
            "...........................\n"
            "......o..............o.....\n"
            "..o.......o................\n",
        ),
        ("1x1 empty", "1.ox\n.\n"),
        ("1x1 obstacle", "1.ox\no\n"),
        ("3x3 all empty", "3.ox\n...\n...\n...\n"),
        ("3x3 all obstacles", "3.ox\nooo\nooo\nooo\n"),
        ("single row", "1.ox\n..o....\n"),
        ("single column", "5.ox\n.\n.\no\n.\n.\n"),
        (
            "top/left tie breaking",
            "4.ox\n"
            "....\n"
            "....\n"
            "ooo.\n"
            "....\n",
        ),
        (
            "non-standard symbols",
            "4abc\n"
            "aaaaaa\n"
            "aabaaa\n"
            "aaaaaa\n"
            "aaaaaa\n",
        ),
        (
            "digit as obstacle",
            "3.5x\n"
            "..5..\n"
            ".....\n"
            ".....\n",
        ),
        # Important: empty itself is a digit.
        (
            "digit as empty",
            "31ox\n"
            "1111\n"
            "1o11\n"
            "1111\n",
        ),
        (
            "space as empty",
            "3 ox\n"
            "    \n"
            " o  \n"
            "    \n",
        ),
        (
            "full character is digit",
            "4.o7\n"
            ".....\n"
            "..o..\n"
            ".....\n"
            ".....\n",
        ),
    ]


def invalid_cases():
    return [
        ("empty input", ""),
        ("header only", "3.ox\n"),
        ("zero height", "0.ox\n"),
        ("negative height", "-1.ox\n.\n"),
        ("missing height", ".ox\n.\n"),
        ("missing symbol", "3.o\n...\n...\n...\n"),
        ("extra symbol in header", "3.oxQ\n...\n...\n...\n"),
        ("same empty/obstacle", "3..x\n...\n...\n...\n"),
        ("same empty/full", "3.o.\n...\n...\n...\n"),
        ("same obstacle/full", "3.oo\n...\n...\n...\n"),
        ("empty row", "3.ox\n...\n\n...\n"),
        ("wrong width", "3.ox\n...\n....\n...\n"),
        ("invalid cell", "3.ox\n...\n.z.\n...\n"),
        ("too few rows", "3.ox\n...\n...\n"),
        ("too many rows", "2.ox\n...\n...\n...\n"),
        ("missing newline on last row", "3.ox\n...\n...\n..."),
        ("header missing newline", "3.ox"),
        (
            "height includes non-digit",
            "1A.ox\n.\n",
        ),
    ]


def random_case(rng, index):
    h = rng.randint(1, 8)
    w = rng.randint(1, 12)

    symbol_sets = [
        (".", "o", "x"),
        ("_", "#", "@"),
        ("1", "o", "x"),
        (" ", "o", "X"),
        ("a", "5", "Z"),
    ]
    empty, obstacle, full = rng.choice(symbol_sets)

    rows = []
    for _ in range(h):
        row = "".join(obstacle if rng.random() < 0.22 else empty for _ in range(w))
        rows.append(row)

    return (
        f"random #{index} ({h}x{w}, symbols={empty!r}/{obstacle!r}/{full!r})",
        f"{h}{empty}{obstacle}{full}\n" + "".join(r + "\n" for r in rows),
    )


def show_diff(expected, got):
    print("      expected:", repr(expected))
    print("      got     :", repr(got))


def test_case(binary, name, content, as_file):
    expected = solve_reference(content)
    got, stderr, rc, err = run(binary, content, as_file=as_file)

    if err:
        return False, f"{err}"

    if got != expected:
        show_diff(expected, got)
        if stderr:
            print("      stderr  :", repr(stderr))
        return False, f"return code={rc}"

    return True, None


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <bsq_binary>")
        return 1

    binary = sys.argv[1]
    if "/" not in binary:
        binary = "./" + binary

    if not os.path.isfile(binary) or not os.access(binary, os.X_OK):
        print(f"{RED}Executable not found: {binary}{RESET}")
        return 1

    passed = 0
    failed = 0

    cases = []
    for name, content in valid_cases():
        cases.append((name, content))
    for name, content in invalid_cases():
        cases.append((name, content))

    rng = random.Random(42)
    for i in range(1, 31):
        cases.append(random_case(rng, i))

    print(f"{BOLD}{CYAN}BSQ extended tester{RESET}")
    print(f"binary: {binary}\n")

    for mode in ("stdin", "file"):
        print(f"{BOLD}[ {mode} ]{RESET}")
        as_file = mode == "file"

        for name, content in cases:
            ok, info = test_case(binary, name, content, as_file)
            if ok:
                print(f"  {GREEN}PASS{RESET} {name}")
                passed += 1
            else:
                print(f"  {RED}FAIL{RESET} {name} ({info})")
                failed += 1

    print(f"\n{BOLD}[ other errors ]{RESET}")

    # Missing file is not an invalid-map error; the subject asks for a meaningful Error: message.
    missing = "/tmp/this_bsq_file_should_not_exist_42"
    got, _, _, err = run(binary, args=[missing])
    if not err and got.startswith("Error:"):
        print(f"  {GREEN}PASS{RESET} missing file produces a meaningful Error: message")
        passed += 1
    else:
        print(f"  {RED}FAIL{RESET} missing file error handling: {repr(got)}")
        failed += 1

    # More than one argument: exact wording is implementation-dependent,
    # but it should be an Error: message rather than normal map output.
    got, _, _, err = run(binary, args=["one", "two"])
    if not err and got.startswith("Error:"):
        print(f"  {GREEN}PASS{RESET} extra arguments produce an Error: message")
        passed += 1
    else:
        print(f"  {YELLOW}WARN{RESET} extra arguments: {repr(got)}")

    total = passed + failed
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    color = GREEN if failed == 0 else RED
    print(f"{color}{BOLD}{passed}/{total} strict checks passed{RESET}")

    if failed:
        print(
            f"\n{YELLOW}Tip:{RESET} the subject requires the exact invalid-map text "
            f"{ERROR.strip()!r}."
        )

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
