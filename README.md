# Advent of Code 22

Solutions for the advent of code 2022 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2022

## Python

Iterate a list in groups of size `N`:

```
for group in (items[i:i + N] for i in range(0, len(items), N)):
    pass
```

Avoid `eval()` or at least use `ast.literal_eval()` instead.

## Math


### Modulo

Modulo plays nice with multiplication and addition, see modulo rules. This means that performing a
lot of additions and multiplications of a number then taking modulo `N` gives the same result as
performing modulo `N` after each operation. This can be helpful if the operations would create a
huge number and we are only interested of the modulo `N` of this number.

To keep track of a number `X` modulo any number in a set of numbers `{N1, N2, ..., Nn}` we can use
the same principle as above but use `N1*N2*...Nn` as `N` (or rather the least common multiple of the
`N`s). This means that by performing `X` modulo `N` after each operation, then performing `X`
modulo `Ni` will give the expected (correct) result.

### Rotate Matrix 45 Degrees

Rotating a square matrix 45 degrees can be done as follows:

```
M_rot[x - y][x + y] = M[y][x],
```

i.e.

```
x' = x + y
y' = x - y
```

To rotate back use the following equations:

```
x = (x' + y') // 2
y = (x' - y') // 2
```

Note that the rotated matrix will be translated, see
[this](https://math.stackexchange.com/questions/732679/how-to-rotate-a-matrix-by-45-degrees) for
more information.
