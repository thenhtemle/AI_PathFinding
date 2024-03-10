from Graph import Graph
from collections import deque


input_path = None
graph = None


try:
    input_path = input("Enter the name of the input file: ")
    graph = Graph(input_path, "BFS")
except Exception as e:
    print(repr(e))
    quit()


expanded = graph.expand()
if expanded is None:
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
