# Advent of Code 22

Solutions for the advent of code 2022 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2022

A potentially good algorithms book: https://jeffe.cs.illinois.edu/teaching/algorithms/

## Algorithms

### Path Finding

A useful trick if using `heapq` as priority queue (for e.g. Dijkstra or A star) is to use
`(priority, priority_counter)` as priority instead of just `priority`. Then each priority will be
unique and the "data" part of the tuple will not be used for comparison (the data part may not have
support for comparison). For an example see day 24.

Dijkstra is basically breadth first search with a priority queue that selects the closest nodes
first. A* is an extension of Dijkstra and uses an additional heuristic to add to the priorities.
An example heuristic is the Manhattan distance to the end node.

Some guidelines for path finding algorithms:

* Use breadth first search if all edges has equal cost
* Use Dijkstra if the edges have different costs.
* A* can be used to speed up both BFS and Dijkstra if one can come up with a heuristic to guide
  the selection of next step to the right direction

A changing 2D grid/map may be seen as a 3D grid/map, especially if there is a cyclic behavior in
the changes of the 2D map.

### Binary Search

See `algorithms.py` for details (note that this implementations assumes items to be ordered in
descending order). Can be used to e.f. finding the root of a function (known as the bisection
method).

### Cycle Detection

To detect a cycle:

1. Determine what the `state` is, i.e. the things needed to determine if a certain set of conditions
   has occurred before.
2. For each iteration check if the current `state` is in `visited` states.
3. If false, add current `state` to visited.
4. If true, cycle detected. If conditions from the previous time this `state` occurred are needed
   use a dict for `visited` where the keys are the `state` and the conditions are the keys.

See day 17 for an example.

### Circular Doubly Linked List

See `algorithms.py` for an example how how to create a circular double linked list.

### Cube

There is a method called "cube mapping" that uses the six faces of a cube as tiles. It is then
possible to convert between a `(x, y, z)` coordinate on the surface of the cube and a `(face, u, v)`
coordinate of a tile/face. See https://en.wikipedia.org/wiki/Cube_mapping for more details.

<img src="adventofcode/day22/cube_fold.png" width="400"/>

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

### Complex Numbers

It is useful to represent a 2D coordinate system using complex numbers. Translations can then
easily be performed with complex addition and rotation can be performed by complex multiplication.
To rotate clockwise multiply the coordinate/vector by `i`, to rotate counter clockwise multiply by
`-i`. See day 22 for an example.

### Modulo

Modulo plays nice with multiplication and addition, see modulo rules. This means that performing a
lot of additions and multiplications of a number then taking modulo `N` gives the same result as
performing modulo `N` after each operation. This can be helpful if the operations would create a
huge number and we are only interested of the modulo `N` of this number.

To keep track of a number `X` modulo any number in a set of numbers `{N1, N2, ..., Nn}` we can use
the same principle as above but use `N1*N2*...Nn` as `N` (or rather the least common multiple of the
`N`s). This means that by performing `X` modulo `N` after each operation, then performing `X`
modulo `Ni` will give the expected (correct) result.

### Newton's Method

Can be used to find to root (i.e. the x value for which the function is 0) of a function `f`.

```
X0 = initial_guess

Iterate:
    Xn+1 = Xn - f(Xn) / f'(Xn)
```

The idea is to estimate the function as the tangent line at `X` (i.e. `f'(X)`) and calculate
where this estimated function is 0. This is quite simple, all we need to find is where this line
crosses the x-axis. The next `X` is set to this intersection point. Note that this works best for
monotonic functions, more complicated functions may not converge at all due to e.g. a bad initial
estimate or due to "overshoot" of the zero point.

If `f'(X)` is difficult to get analytically it can be estimated as:

```
def derivative(f, x, h=1):
    return (f(x + h) - f(x)) / h
```

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

## Visualization

ffmpeg can be used to create nice visualizations: https://sjmulder.nl/2022/aoc-ffmpeg.html
