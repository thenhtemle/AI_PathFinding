from Graph import Graph
import itertools

graph = Graph("input.txt", "A_Star")

stops = graph.get_stops()
stops_permutations = itertools.permutations(stops, len(stops))

start = graph.get_start()
goal = graph.get_goal()

final_path = []
final_cost = float("inf")
stops_inorder = []

for perm in stops_permutations:
    total_cost = 0
    path = []
    stops_list = []
    temp_start = start
    
    for stop in perm:
        path_tuple = graph.find_shortest_path(temp_start, stop)
        total_cost += path_tuple[1]
        temp_start = stop
        path.append(path_tuple[0])
        stops_list.append(stop)

    path_tuple = graph.find_shortest_path(temp_start, goal)
    total_cost += path_tuple[1]
    path.append(path_tuple[0])

    if total_cost < final_cost:
        final_cost = total_cost
        final_path = path
        stops_inorder = stops_list  

      
start = graph.get_start()
for segment in final_path:
    for i in range(1, len(segment)):
        if i-1 != 0:
            graph.set_path(segment[i-1])
        graph.set_cur_pos(segment[i])
        graph.add_state()

graph.output_animation()
