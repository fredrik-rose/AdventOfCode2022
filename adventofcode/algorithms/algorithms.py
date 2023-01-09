import collections as coll


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def remove(self):
        left = self.left
        right = self.right
        if left:
            left.right = right
        if right:
            right.left = left
        self.left = None
        self.right = None

    def insert_right(self, node):
        right = self.right
        self.right = node
        right.left = node
        node.left = self
        node.right = right

    def __repr__(self):
        return f"{self.left.value} <- {self.value} -> {self.right.value}"


def create_circular_doubly_linked_list(items):
    first = Node(items[0])
    prev = first
    for element in items[1:]:
        node = Node(element)
        node.left = prev
        prev.right = node
        prev = node
    first.left = prev
    prev.right = first
    return first


def newtons_method(f, x0, steps, df_dx=None):
    if df_dx is None:
        df_dx = lambda x: derivative(f, x)
    x = x0
    for _ in range(steps):
        if f(x) == 0:
            return x
        x = x - f(x) / df_dx(x)
    return x


def derivative(f, x, h=1):
    return (f(x + h) - f(x)) / h


def binary_search_descening_order(get_item, target, low, high):
    if high < low:
        return None
    mid = (high + low) // 2
    value = get_item(mid)  # get_item is a function, an alternative is to pass in a list 'items' and use items[mid].
    if value == target:
        return mid
    # Swap the comparisons below if the items are ordered in ascending order.
    elif target > value:
        return binary_search_descening_order(get_item, target, low, mid - 1)
    elif target < value:
        return binary_search_descening_order(get_item, target, mid + 1, high)
    assert False


def breadth_first_search(graph, start, end, neighbors_generator):
    visited = set(start)
    queue = coll.deque([(start, 0)])
    while queue:
        node, distance = queue.popleft()
        if node == end:
            return distance
        for neighbor in neighbors_generator(graph, node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    return None
