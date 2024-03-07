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
    val, h, p, par = heapq.heappop(wait_list)
    if not graph.is_explored(p):
        graph.set_parent(p, par)
    else:
        continue

    expanded = graph.expand(p)
    if expanded is None:
        found = True
        break

    g = val - h + 1
    dfs_stack = []
    min_value_threshold = max(val, min_value_threshold)

    for new_p in expanded[0] + expanded[1]:
        h = graph.hueristic(new_p)
        dfs_stack.append((g + h, h, new_p, p))

    while len(dfs_stack) != 0:
        val, h, p, par = dfs_stack.pop()

        if val > min_value_threshold:
            heapq.heappush(wait_list, (val, h, p, par))
            continue

        if not graph.is_explored(p):
            graph.set_parent(p, par)
        else:
            continue

        expanded = graph.expand(p)

        if expanded is None:
            found = True
            break

        g = val - h + 1
        for new_p in expanded[0] + expanded[1]:
            h = graph.hueristic(new_p)
            dfs_stack.append((g + h, h, new_p, p))


if not found:
    graph.give_up()