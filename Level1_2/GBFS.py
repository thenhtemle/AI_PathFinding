from Graph import Graph
import heapq


input_path = None
graph = None


try:
    input_path = input("Enter the name of the input file: ")
    graph = Graph(input_path, "GBFS")
except Exception as e:
    print(repr(e))
    quit()
print()


found: bool = False

start = graph.get_start()
frontier = [(graph.hueristic(start), 0, start)]


while len(frontier) != 0:  # Duyệt cho đến hết stack
    h, g, p = heapq.heappop(frontier)

    expanded = graph.expand(p)  # Expand điểm đó
    if expanded is None:  # Nếu đã tìm ra đường đi thì dừng
        found = True
        break

    for new_p in expanded[0]:
        heapq.heappush(frontier, (graph.hueristic(new_p), g + 1, new_p))

if not found:  # Nếu không tìm thấy đường đi thì give up...
    graph.give_up()
