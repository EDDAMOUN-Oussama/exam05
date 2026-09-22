#!/usr/bin/env python3
"""
Tester for the 42 'bsq' exercise.
Usage:
    python3 test.py ./a.out
"""

import subprocess
import sys
import os
import tempfile

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

# ─── Reference solver ────────────────────────────────────────────────────────

def solve_bsq(content: str):
    """
    Pure Python reference implementation of bsq.
    Returns the output string (solved map or error message).
    """
    lines = content.split('\n')
    if not lines:
        return "Error: invalid map\n"

    header = lines[0]

    # Parse height
    i = 0
    height_str = ""
    while i < len(header) and header[i].isdigit():
        height_str += header[i]
        i += 1

    if not height_str:
        return "Error: invalid map\n"

    height = int(height_str)
    if height <= 0:
        return "Error: invalid map\n"

    # Parse 3 chars
    if i + 3 > len(header):
        return "Error: invalid map\n"

    empty_c  = header[i];   i += 1
    obs_c    = header[i];   i += 1
    full_c   = header[i];   i += 1

    # Nothing allowed after the 3 chars (header ends here — no trailing chars)
    if i < len(header) and header[i] not in ('', '\r'):
        return "Error: invalid map\n"

    # chars must be distinct and printable (32-126)
    for c in (empty_c, obs_c, full_c):
        if ord(c) < 32 or ord(c) > 126:
            return "Error: invalid map\n"
    if len({empty_c, obs_c, full_c}) != 3:
        return "Error: invalid map\n"

    # Read map rows (lines[1..height])
    map_rows = lines[1:height + 1]
    if len(map_rows) != height:
        return "Error: invalid map\n"

    grid = []
    width = None
    for row in map_rows:
        # Strip trailing \r if present
        if row.endswith('\r'):
            row = row[:-1]
        if width is None:
            width = len(row)
        if len(row) != width or width == 0:
            return "Error: invalid map\n"
        for c in row:
            if c != empty_c and c != obs_c:
                return "Error: invalid map\n"
        grid.append(list(row))

    # DP: largest square
    dp = [[0] * width for _ in range(height)]
    best_size, best_r, best_c = 0, 0, 0

    for r in range(height):
        for c in range(width):
            if grid[r][c] == obs_c:
                dp[r][c] = 0
            elif r == 0 or c == 0:
                dp[r][c] = 1
            else:
                dp[r][c] = 1 + min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1])

            if dp[r][c] > best_size:
                best_size = dp[r][c]
                best_r = r - best_size + 1
                best_c = c - best_size + 1

    # Fill square
    for r in range(best_r, best_r + best_size):
        for c in range(best_c, best_c + best_size):
            grid[r][c] = full_c

    result = ""
    for row in grid:
        result += ''.join(row) + '\n'
    return result


# ─── Run binary ──────────────────────────────────────────────────────────────

def run_via_stdin(binary, content, timeout=5.0):
    try:
        r = subprocess.run(
            [binary],
            input=content,
            capture_output=True, text=True, timeout=timeout
        )
        return r.stdout, r.returncode, None
    except subprocess.TimeoutExpired:
        return None, None, "TIMEOUT"

def run_via_file(binary, content, timeout=5.0):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(content)
            fname = f.name
        r = subprocess.run(
            [binary, fname],
            input='', capture_output=True, text=True, timeout=timeout
        )
        os.unlink(fname)
        return r.stdout, r.returncode, None
    except subprocess.TimeoutExpired:
        return None, None, "TIMEOUT"
    except Exception as e:
        return None, None, str(e)


# ─── Tests ───────────────────────────────────────────────────────────────────

VALID_MAPS = [
    # (name, map_content)

    # Subject example
    ("Subject example (9 rows)",
     "9.ox\n"
     "...........................\n"
     "....o......................\n"
     "............o..............\n"
     "...........................\n"
     "....o......................\n"
     "...............o...........\n"
     "...........................\n"
     "......o..............o.....\n"
     "..o.......o................\n"),

    # Simple 3x3 all empty
    ("3x3 all empty",
     "3.ox\n...\n...\n...\n"),

    # 1x1 empty
    ("1x1 empty cell",
     "1.ox\n.\n"),

    # 1x1 obstacle
    ("1x1 obstacle",
     "1.ox\no\n"),

    # Blinker-style: single row
    ("1 row, mixed",
     "1.ox\n.o.o...\n"),

    # All obstacles
    ("3x3 all obstacles",
     "3.ox\nooo\nooo\nooo\n"),

    # Obstacle in center
    ("3x3 obstacle in center",
     "3.ox\n...\n.o.\n...\n"),

    # Bigger map with obstacle blocking
    ("5x5 obstacle blocks top-left",
     "5.ox\no....\n.....\n.....\n.....\n.....\n"),

    # Non-standard chars
    ("Non-standard chars (a, b, c)",
     "3abc\naaa\naaa\naaa\n"),

    # Number as empty char (tricky for fscanf-based parsers)
    # header "3 ox" — but space might not be printable per some impls
    # Use digit as obstacle instead (safe)
    ("Digit as obstacle char",
     "2.5x\n.5.\n...\n"),

    # Space as empty char — kills fscanf-based parsers (the \n in "%d%c%c%c\n" eats leading spaces)
    ("Space as empty char",
     "3 ox\n o \n o \n o \n"),

    # Wide map (1 row)
    ("1 row wide",
     "1.ox\n...................\n"),

    # Tall map (1 col)
    ("Tall 1 col",
     "5.ox\n.\n.\n.\n.\n.\n"),

    # Square already in top-left preference
    ("Top-left preference",
     "4.ox\n....\n....\n..o.\n....\n"),

    # Tie: two equal squares — pick topmost then leftmost
    ("Tie: two 2x2 squares",
     "4.ox\n....\n....\nooo.\n....\n"),

    # Full square (no obstacles)
    ("4x4 no obstacles",
     "4.ox\n....\n....\n....\n....\n"),
]

INVALID_MAPS = [
    # (name, content, description)
    ("Empty input",            "",                               "no data"),
    ("No newline at end",      "3.ox\n...\n...\n...",            "missing final newline — behavior may vary"),
    ("Height 0",               "0.ox\n",                        "height=0"),
    ("Negative height",        "-1.ox\n.\n",                    "negative height"),
    ("No height",              ".ox\n.\n",                      "missing height"),
    ("Duplicate chars (e==o)", "3.ox\n" + "...\n"*3,            "this is valid actually"),  # actually valid
    ("Same empty and obs",     "3..x\n...\n...\n...\n",         "empty==obstacle"),
    ("Same empty and full",    "3.xo\n" + "...\n"*3,            "actually valid, different chars"),
    ("All three same",         "3...\n...\n...\n...\n",         "all chars identical"),
    ("Extra char in header",   "3.oxx\n...\n...\n...\n",        "extra char after full"),
    ("Too few rows",           "3.ox\n...\n...\n",              "only 2 rows instead of 3"),
    ("Row width mismatch",     "3.ox\n...\n....\n...\n",        "rows differ in width"),
    ("Invalid char in map",    "3.ox\n.z.\n...\n...\n",        "unknown char"),
    ("Empty row",              "3.ox\n\n...\n...\n",            "empty row"),
    ("Missing chars in header","3.\n...\n...\n...\n",           "only 1 char after height"),
]


# ─── Runner ──────────────────────────────────────────────────────────────────

def run_test_valid(binary, name, content, use_file=False):
    expected = solve_bsq(content)
    runner = run_via_file if use_file else run_via_stdin
    got, rc, err = runner(binary, content)

    if err:
        return False, expected, None, f"ERROR: {err}"
    if got == expected:
        return True, expected, got, None
    return False, expected, got, None


def print_header(text):
    print(f"\n{BOLD}{CYAN}{'═'*62}{RESET}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{BOLD}{CYAN}{'═'*62}{RESET}")


def show_diff(expected, got):
    exp_lines = expected.splitlines()
    got_lines = (got or "").splitlines()
    while len(got_lines) < len(exp_lines):
        got_lines.append('')
    while len(exp_lines) < len(got_lines):
        exp_lines.append('')
    w = max((len(l) for l in exp_lines), default=10)
    print(f"  {'EXPECTED':^{w+4}}    {'GOT':^{w+4}}")
    for e, g in zip(exp_lines, got_lines):
        marker = "  " if e == g else "!!"
        print(f"  |{e:<{w}}|  {marker}  |{g:<{w}}|")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <binary>")
        sys.exit(1)

    binary = sys.argv[1]
    if os.sep not in binary and not binary.startswith('.'):
        binary = './' + binary
    if not os.path.isfile(binary):
        print(f"{RED}Binary not found: {binary}{RESET}")
        sys.exit(1)
    if not os.access(binary, os.X_OK):
        print(f"{RED}Not executable: {binary}{RESET}")
        sys.exit(1)

    passed = failed = 0
    failures = []

    # ── Valid maps via STDIN ─────────────────────────────────────────────
    print_header(f"Testing: {binary}")
    print(f"\n{BOLD}[ Valid Maps — stdin ]{RESET}")

    for name, content in VALID_MAPS:
        ok, expected, got, err = run_test_valid(binary, name, content, use_file=False)
        if err:
            print(f"  {RED}ERR {RESET}  {name}")
            failed += 1
            failures.append((name + " [stdin]", expected, None, err))
        elif ok:
            print(f"  {GREEN}PASS{RESET}  {name}")
            passed += 1
        else:
            print(f"  {RED}FAIL{RESET}  {name}")
            failed += 1
            failures.append((name + " [stdin]", expected, got, None))

    # ── Valid maps via FILE arg ──────────────────────────────────────────
    print(f"\n{BOLD}[ Valid Maps — file arg ]{RESET}")

    for name, content in VALID_MAPS:
        ok, expected, got, err = run_test_valid(binary, name, content, use_file=True)
        if err:
            print(f"  {RED}ERR {RESET}  {name}")
            failed += 1
            failures.append((name + " [file]", expected, None, err))
        elif ok:
            print(f"  {GREEN}PASS{RESET}  {name}")
            passed += 1
        else:
            print(f"  {RED}FAIL{RESET}  {name}")
            failed += 1
            failures.append((name + " [file]", expected, got, None))

    # ── Invalid maps — expect "Error: invalid map\n" ─────────────────────
    print(f"\n{BOLD}[ Invalid Maps — should print 'Error: invalid map' ]{RESET}")

    for name, content, desc in INVALID_MAPS:
        expected = solve_bsq(content)
        # Skip cases where our reference says it's actually valid
        if not expected.startswith("Error:"):
            print(f"  {YELLOW}SKIP{RESET}  {name}  ({desc})")
            continue

        got, _, err = run_via_stdin(binary, content)
        if err:
            print(f"  {RED}ERR {RESET}  {name}  [{desc}]")
            failed += 1
        elif got and got.startswith("Error:"):
            print(f"  {GREEN}PASS{RESET}  {name}  [{desc}]")
            passed += 1
        else:
            print(f"  {RED}FAIL{RESET}  {name}  [{desc}]")
            print(f"         got: {repr(got)}")
            failed += 1
            failures.append((name, "Error: invalid map\n", got, None))

    # ── File-not-found ───────────────────────────────────────────────────
    print(f"\n{BOLD}[ File Error Handling ]{RESET}")
    try:
        r = subprocess.run([binary, "/tmp/does_not_exist_bsq_42.txt"],
                           capture_output=True, text=True, timeout=3)
        if r.stdout.startswith("Error:"):
            print(f"  {GREEN}PASS{RESET}  File not found → Error message")
            passed += 1
        else:
            print(f"  {RED}FAIL{RESET}  File not found → got: {repr(r.stdout)}")
            failed += 1
    except Exception as e:
        print(f"  {RED}ERR {RESET}  {e}")
        failed += 1

    # ── Summary ──────────────────────────────────────────────────────────
    total = passed + failed
    print_header("Results")
    color = GREEN if failed == 0 else RED
    print(f"  {color}{BOLD}{passed}/{total} passed{RESET}")

    if failures:
        print(f"\n{BOLD}[ Failure Details ]{RESET}")
        for name, expected, got, err in failures:
            print(f"\n  {RED}✗ {name}{RESET}")
            if err:
                print(f"    {err}")
            else:
                show_diff(expected, got or "")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()