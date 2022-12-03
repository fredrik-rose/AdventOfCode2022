# Advent of Code 22

Solutions for the advent of code 2022 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2022

## Python

Iterate a list in groups of size `N`:

```
for group in (items[i:i + N] for i in range(0, len(items), N)):
    pass
```
