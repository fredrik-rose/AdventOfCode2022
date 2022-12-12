import collections as coll

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
