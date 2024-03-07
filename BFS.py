import Graph
from collections import deque

graph = Graph.Graph(
    "input.txt", "BFS"
)  

found: bool = False

queue = [(p, graph.get_start()) for p in graph.expand()[0]]

while queue:  
    p, par = queue.popleft()  
    if graph.is_explored(p): 
        continue

    graph.set_parent(p, par)  
    expanded = graph.expand(p)  

    if expanded is None:  
        found = True
        break

    for new_p in (
        expanded[0] + expanded[1]
    ):  
        queue.append((new_p, p))

if not found:  
    graph.give_up()
