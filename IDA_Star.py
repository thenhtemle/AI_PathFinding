import Graph
import heapq


graph = Graph.Graph("input2.txt", "IDA_Star")
wait_list = []
start = graph.get_start()
expanded = graph.expand()

if expanded is None:
    quit()

for p in expanded[0]:
    h = graph.hueristic(p)
    heapq.heappush(wait_list, (1 + h, h, p, start))
min_value_threshold = 0

found = False
while len(wait_list) != 0 and not found:
    f, h, p, par = heapq.heappop(wait_list)
    if graph.is_explored(p):
        continue

    graph.set_parent(p, par)
    expanded = graph.expand(p)
    if expanded is None:
        found = True
        break

    g = f - h + 1
    dfs_stack = []
    min_value_threshold = max(f, min_value_threshold)

    for new_p in expanded[0] + expanded[1]:
        dfs_stack.append((g, new_p, p))

    while len(dfs_stack) != 0:
        g, p, par = dfs_stack.pop()
        h = graph.hueristic(p)

        if g + h > min_value_threshold:
            heapq.heappush(wait_list, (g + h, h, p, par))
            continue

        if graph.is_explored(p):
            continue

        graph.set_parent(p, par)
        expanded = graph.expand(p)

        if expanded is None:
            found = True
            break

        for new_p in expanded[0] + expanded[1]:
            dfs_stack.append((g + 1, new_p, p))


if not found:
    graph.give_up()
