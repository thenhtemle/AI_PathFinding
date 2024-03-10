import Graph_Advanced as Graph
import itertools
from collections import deque


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


graph = Graph.Graph("input.txt", "BFS_Advanced")

#Cờ found để kiểm tra xem đã tìm được đường đi chưa, lúc đầu gán = False
found: bool = False

#Danh sách các điểm đón
stops = graph.get_stops()

#Tạo hoán vị của các điểm đón
permutations = itertools.permutations(stops)
    
#Tạo biến shortest_path và shortest_distance để lưu đường đi ngắn nhất và độ dài của nó
shortest_path = None
shortest_distance = 0

#Duyệt qua từng hoán vị
for perm in permutations:
    #Reset lại trạng thái của graph
    graph.reset()

    current_distance = 0
    
    start = graph.get_start()
    goal = graph.get_goal()
    
    current_node = start
    
    for stop in perm:
        # Tìm đường đi từ current_node tới stop
        graph.set_start(current_node)
        graph.set_goal(stop)
        bfs(graph)
        path_to_stop = graph.distance(current_node, stop)[0]
        if path_to_stop == None:
            # Nếu không có đường đi từ current_node tới stop, bỏ qua hoán vị này
            current_distance = 0
            break
        
        # Cập nhật độ dài của đường đi và thêm nó vào current_path
        current_distance += path_to_stop - 1
        
        # Cập nhật current_node cho stop
        current_node = stop
    
    # Tìm đường đi từ stop cuối cùng tới goal
    graph.set_start(current_node)
    graph.set_goal(goal)
    bfs(graph)
    path_to_goal = graph.distance(current_node, goal)
    if path_to_goal == None:
        # Nếu không có đường đi từ stop cuối cùng tới goal, bỏ qua hoán vị này
        current_distance = 0
    else:
        # Cập nhật độ dài của đường đi và thêm nó vào current_path
        current_distance += path_to_goal - 1
        found = True

    
    if current_distance < shortest_distance:
        shortest_distance = current_distance


if not found:
    graph.give_up()


