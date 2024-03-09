import Graph_Advanced as Graph
import itertools
from collections import deque


graph = Graph.Graph("input.txt", "BFS")

# Func to print permutations of a given list, return a list of lists
def permutation(lst):
    if len(lst) == 0:
        return []
    if len(lst) == 1:
        return [lst]
    l = []
    for i in range(len(lst)):
        m = lst[i]
        remLst = lst[:i] + lst[i + 1:]
        for p in permutation(remLst):
            l.append([m] + p)
    return l    


found: bool = False


stops = graph.get_stops()
permutations = itertools.permutations(stops)
    
shortest_path = None
shortest_length = float('inf')

for perm in permutations:
    graph.reset_state()
    current_path = []
    current_length = 0
    
    start = graph.get_start()
    current_node = start
    
    for stop in perm:
        # Tìm đường đi từ current_node tới stop????
        path_to_stop = graph.find_path_bfs(current_node, stop)
        if path_to_stop is None:
            # Nếu không có đường đi từ current_node tới stop, bỏ qua hoán vị này
            current_length = float('inf')
            break
        
        # Cập nhật độ dài của đường đi và thêm nó vào current_path
        current_length += len(path_to_stop) - 1
        current_path.extend(path_to_stop[1:])  # Bỏ qua điểm bắt đầu
        
        # Cập nhật current_node cho stop
        current_node = stop
    
    
    if current_length < shortest_length:
        shortest_length = current_length
        shortest_path = current_path


if not found:
    graph.give_up()


