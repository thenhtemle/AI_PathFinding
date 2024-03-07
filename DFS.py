import Graph


graph = Graph.Graph(
    "input.txt", "DFS"
)  # Tạo graph từ file input.txt để chạy thuật toán DFS


found: bool = False

stack = [(p, graph.get_start()) for p in graph.expand()[0]]
# Stack lưu các đỉnh sắp được mở rộng. Stack vì là DFS... Expand đỉnh đầu tiên. Lưu thêm đỉnh trước (parent) của nó

while len(stack) != 0:  # Duyệt cho đến hết stack
    p, par = stack.pop()  # Lấy phần tử trên cùng
    if graph.is_explored(p):  # Nếu đỉnh đã đi qua thì thôi...
        continue

    graph.set_parent(p, par)  # Nếu không thì cập nhật đỉnh kề trước nó
    expanded = graph.expand(p)  # Expand điểm đó

    if expanded is None:  # Nếu đã tìm ra đường đi thì dừng
        found = True
        break

    for new_p in (
        expanded[0] + expanded[1]
    ):  # Nếu không thì thêm những điểm vừa được expanded vào stack
        stack.append((new_p, p))

if not found:  # Nếu không tìm thấy đường đi thì give up...
    graph.give_up()