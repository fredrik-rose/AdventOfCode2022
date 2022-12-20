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
