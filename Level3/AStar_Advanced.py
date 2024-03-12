# from heapq import *
# from CSC14003.AI_PathFinding.Level3.Graph import Graph


# def AStar(graph: Graph):
#     open_set = set()
#     closed_set = set()

#     g_score = {graph.get_start(): 0}
#     f_score = {graph.get_start(): graph.hueristic(graph.get_start())}

#     open_set.add(graph.get_start())

#     while open_set:
#         cur = min(open_set, key=lambda x: f_score[x])

#         if cur == graph.get_goal():
#             return graph.get_path(cur)

#         open_set.remove(cur)
#         closed_set.add(cur)

#         neighbors, _ = graph.expand(cur)
#         for neighbor in neighbors:
#             if neighbor in closed_set:
#                 continue

#             tentative_g_score = g_score[cur] + 1

#             if neighbor not in open_set or tentative_g_score < g_score[neighbor]:
#                 graph.set_parent(neighbor, cur)
#                 g_score[neighbor] = tentative_g_score
#                 f_score[neighbor] = g_score[neighbor] + graph.hueristic(neighbor)

#                 if neighbor not in open_set:
#                     open_set.add(neighbor)
#     return None


# def AStar_Advanced(graph: Graph):
#     # Danh sách các điểm đón đã đi qua
#     visited = []
#     # Đường đi cần tìm
#     finalPath = []

#     start = graph.get_start()
#     goal = graph.get_goal()
#     stops = graph.get_stops()
#     distance = len(stops)

#     totalCost = 0
#     while distance > 0:
#         # Đường đi ngắn nhất từ điểm đang xét đến các điểm đón chưa đi qua
#         routes = {}
#         # Dùng priority queue để lưu điểm đón và chi phí từ điểm đang xét đến nó
#         priority_queue = []

#         for stop in stops:
#             if stop not in visited:
#                 graph.set_start(start)
#                 graph.set_goal(stop)

#                 # Đường đi ngắn nhất từ điểm đang xét đến
#                 path = AStar(graph)
#                 if path == False:  # Không tìm thấy đường đi
#                     return (-1, False)

#                 routes[stop] = path
#                 heappush(priority_queue, (len(path) - graph.hueristic(stop), stop))

#         # Cho ra điểm có chi phí nhỏ nhất
#         cost, stopPoint = heappop(priority_queue)
#         totalCost += cost
#         finalPath += routes[stopPoint]

#         # Đánh dấu đã đi qua điểm đón
#         visited.append(stopPoint)
#         start = stopPoint
#         distance -= 1

#     # Tìm lộ trình từ điểm đón cuối dùng đến đích
#     graph.set_start(start)
#     graph.set_goal(goal)
#     path = AStar(graph)
#     if path == False:
#         return (-1, False)
#     sumCost += len(path)
#     finalPath += path

#     # Trả về tổng chi phí và lộ trình
#     return (sumCost, finalPath)


# input_path = None
# graph = None


# try:
#     input_path = input("Enter the name of the input file: ")
#     graph = Graph(input_path, "AStar_Advanced")
# except Exception as e:
#     print(repr(e))
#     quit()


from Graph import Graph

graph = Graph("input.txt", "A_Star")
print(graph.find_shortest_path(graph.get_start(), graph.get_goal()))
