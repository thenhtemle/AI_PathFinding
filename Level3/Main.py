from Graph import Graph
import itertools


input_path = None
graph = None

try:
    input_path = input("Enter the name of the input file: ")
    graph = Graph(input_path, "A_Star")
except Exception as e:
    print(repr(e))
    quit()

stops = graph.get_stops()
stops_permutations = itertools.permutations(stops)

start = graph.get_start()
goal = graph.get_goal()

graph_points = [start] + graph.get_stops() + [goal]

distance_matrix = {p: {} for p in graph_points}
for point1 in graph_points:
    for point2 in graph_points:
        movement = graph.find_shortest_path(point1, point2)
        distance_matrix[point1][point2] = movement

final_path = []
final_cost = float("inf")
stops_inorder = []

for perm in stops_permutations:
    points = list(perm) + [goal]
    total_cost = 0
    path = []
    temp_start = start

    for stop in points:
        movement = distance_matrix[temp_start][stop]
        if movement is None:
            total_cost = float("inf")
            break

        total_cost += movement[1]
        path.append(movement[0])
        temp_start = stop

    if total_cost < final_cost:
        final_cost = total_cost
        final_path = path
        stops_inorder = perm


print()
if final_cost == float("inf"):
    print("No path found.")
    graph.output_animation()
    quit()


print(f"Found path: {tuple(reversed(start))}", end=" ")
for point in stops_inorder:
    print(f"-> {tuple(reversed(point))}", end=" ")
print(f"-> {tuple(reversed(goal))}.")

print(f"Path length: {total_cost}.")


for segment in final_path:
    for i in range(1, len(segment)):
        if i - 1 != 0:
            graph.set_path(segment[i - 1])
        graph.set_cur_pos(segment[i])
        graph.add_state()

graph.output_animation()
