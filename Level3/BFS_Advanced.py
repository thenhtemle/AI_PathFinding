import Graph_Advanced as Graph
import itertools
from collections import deque

graph = Graph.Graph("input.txt", "BFS_Advanced")

#BFS
def bfs(graph):
    expanded = graph.expand()
    if graph is None:
        quit()
    queue = deque(expanded[0])

    while queue:
        p = queue.popleft()
        expanded = graph.expand(p)

        if expanded is None:
            break

        for new_p in expanded[0]:
            queue.append(new_p)

    graph.give_up()

#Cờ found để kiểm tra xem đã tìm được đường đi chưa, lúc đầu gán = False
found: bool = False

#Danh sách các điểm đón
stops = graph.get_stops()
#Tạo hoán vị của các điểm đón
permutations = itertools.permutations(stops)
    
#Tạo biến shortest_path và shortest_length để lưu đường đi ngắn nhất và độ dài của nó
shortest_path = None
shortest_length = 0

#Duyệt qua từng hoán vị
for perm in permutations:
    #Reset lại trạng thái của graph
    graph = Graph.Graph("input.txt", "BFS_Advanced")

    current_length = 0
    
    start = graph.get_start()
    goal = graph.get_goal()
    
    current_node = start
    
    for stop in perm:
        # Tìm đường đi từ current_node tới stop????
        graph.set_start(current_node)
        graph.set_goal(stop)
        bfs(graph)
        path_to_stop = graph.get_visited()
        if path_to_stop == 0:
            # Nếu không có đường đi từ current_node tới stop, bỏ qua hoán vị này
            current_length = 0
            break
        
        # Cập nhật độ dài của đường đi và thêm nó vào current_path
        current_length += path_to_stop - 1
        
        # Cập nhật current_node cho stop
        current_node = stop
    
    # Tìm đường đi từ stop cuối cùng tới goal
    graph.set_start(current_node)
    graph.set_goal(goal)
    bfs(graph)
    path_to_goal = graph.get_visited()
    if path_to_goal == 0:
        # Nếu không có đường đi từ stop cuối cùng tới goal, bỏ qua hoán vị này
        current_length = 0
    else:
        # Cập nhật độ dài của đường đi và thêm nó vào current_path
        current_length += path_to_goal - 1
        found = True

    
    if current_length < shortest_length:
        shortest_length = current_length


if not found:
    graph.give_up()


