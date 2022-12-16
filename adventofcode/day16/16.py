# Day 16: Proboscidea Volcanium
import re


def main():
    graph = parse("16.txt")
    print_graph(graph, "full")
    simplify(graph)
    print_graph(graph, "simple")
    graph, start = rename_to_int(graph)
    print_cpp(graph, start)
    print("Data for the C++ has been generated. Compile and run with:")
    print("    g++ -std=c++17 16.cpp -o 16 && ./16")
    print("To generate the graphs run:")
    print("    dot -Tpng -o graph_simple.png graph_simple.dot && dot -Tpng -o graph_full.png graph_full.dot")


def parse(file_path):
    graph = {}
    with open(file_path) as file:
        for line in file:
            data = line.strip().split(" ")
            node = data[1]
            flow_rate = extract_ints(data[4])[0]
            neighbors = {e[0:2]: 1 for e in data[9:]}
            graph[node] = [flow_rate, neighbors]
    return graph


def extract_ints(text):
    return [int(x) for x in re.findall(r'-?\d+', text)]


def simplify(graph):
    remove = set()
    for node, data in graph.items():
        if node == "AA":
            continue
        flow_rate = data[0]
        if flow_rate > 0:
            continue
        remove_node(graph, node)
        remove.add(node)
    for node in remove:
        del graph[node]


def remove_node(graph, node):
    neighbors = graph[node][1]
    for neighbor in neighbors.keys():
        n_data = graph[neighbor][1]
        for n, d in neighbors.items():
            if n == neighbor:
                continue
            assert n not in n_data
            n_data[n] = n_data[node] + d
            del n_data[node]


def rename_to_int(graph):
    lut = {n: i for i, n in enumerate(graph)}
    new_graph = {lut[n]: v for n, v in graph.items()}
    for node, data in graph.items():
        neighbors = {lut[n]: v for n, v in data[1].items()}
        new_graph[lut[node]] = [data[0], neighbors]
    return new_graph, lut["AA"]


def print_graph(graph, suffix):
    with open(f"graph_{suffix}.dot", "w") as file:
        file.write("digraph graphname {\n")
        for node, data in graph.items():
            for n, c in data[1].items():
                file.write(f'    {node} [label="{node} {data[0]}"];\n')
                file.write(f"    {node} -> {n} [label={c}];\n")
        file.write("}\n")


def print_cpp(graph, start):
    with open("16.hpp", "w") as file:
        file.write("static const std::unordered_map<int, std::vector<std::pair<int, int>>> graph = {\n")
        for node, (_, neighbors) in sorted(graph.items()):
            file.write(f"    {{{node}, {{{', '.join(f'{{{str(n)}, {str(d)}}}' for n, d in neighbors.items())}}}}},\n")
        file.write("};\n")
        flow_rates = []
        for _, (flow_rate, _) in sorted(graph.items()):
            flow_rates.append(flow_rate)
        file.write(f"static const std::vector<int> flow_rates = {{{', '.join(str(e) for e in flow_rates)}}};\n")
        file.write(f"static const int start = {start};\n")


if __name__ == "__main__":
    main()
