import Graph
from collections import deque

graph = Graph.Graph("input3.txt", "BFS")


expanded = graph.expand()
if graph is None:
    quit()
queue = deque(expanded[0])

found: bool = False
while queue:
    p = queue.popleft()
    expanded = graph.expand(p)

    if expanded is None:
        found = True
        break

    for new_p in expanded[0]:
        queue.append(new_p)

if not found:
    graph.give_up()
