from Graph import Graph


input_path = None
graph = None

try:
    input_path = input("Enter the name of the input file: ")
    graph = Graph(input_path, "A_Star")
except Exception as e:
    print(repr(e))
    quit()
print()


start = graph.get_start()
f = {start: (0, 0)}
par = {start: start}
found = False

while len(f) != 0:
    min_node = min(f, key=f.get)
    graph.set_parent(min_node, par[min_node])
    g = f[min_node][1] + 1
    f.pop(min_node)

    expanded = graph.expand(min_node)

    if expanded is None:
        found = True
        break

    for node in expanded[0] + expanded[1]:
        if graph.is_explored(node):
            continue

        if node not in f or g + graph.hueristic(node) < f[node][0]:
            f[node] = (g + graph.hueristic(node), g)
            par[node] = min_node

if not found:
    graph.give_up()
