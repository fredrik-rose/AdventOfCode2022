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

collections.deque is a useful data structure. It has fast remove and insert at both ends and has
support for e.g. rotations.

## C++

For problems that requires speed Python may not cut it. C++ is a good option in these cases as it
fast and has some useful data structures and algorithms as part of the standard. Parsing the input
is however in many cases much easier in Python. An idea is to parse and preprocess the data in
Python and generate a C++ header file to include. The `fscanf()` function may be useful if one
decides to parse in C++. See day 16 for an example.

## DOT

The DOT language is useful for visualizing graphs. See day 16 for an example.

<img src="adventofcode/day16/graph_simple.png" width="800"/>

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
