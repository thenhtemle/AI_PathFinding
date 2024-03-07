from enum import Enum
import numpy as np
from matplotlib import pyplot, colors
import matplotlib.animation as animation
from matplotlib.ticker import MaxNLocator
from time import sleep


class Graph:

    class Status(Enum):
        UNUSED = -1
        UNEXPLORED = 0
        EXPLORED = 1
        FRONTIER = 2
        WALL = 3
        OBSTACLE = 4
        START = 5
        GOAL = 6
        PATH = 7

    def __bound_check(self, x: int, y: int) -> bool:
        return x > 0 and y > 0 and x <= self.__n and y <= self.__m

    def __draw_edge(self, x1: int, y1: int, x2: int, y2: int) -> None:

        if not self.__bound_check(x1, y1) or not self.__bound_check(x2, y2):
            raise ValueError("Obstacle vertex out of bound.")

        def sign(x: int) -> int:
            return 1 if x > 0 else -1

        dx = x2 - x1
        dy = y2 - y1

        self.__grid[x1][y1] = Graph.Status.UNEXPLORED.value

        if dy == 0:
            sign_x = sign(dx)
            for x in range(x1, x2 + sign_x, sign_x):
                if self.__grid[x][y1] != Graph.Status.UNEXPLORED.value:
                    raise ValueError("Invalid edge " + f"({x1} {y1})" f"({x2} {y2})")
                self.__grid[x][y1] = Graph.Status.OBSTACLE.value

            return

        if dx == 0:
            sign_y = sign(dy)
            for y in range(y1, y2 + sign_y, sign_y):
                if self.__grid[x1][y] != Graph.Status.UNEXPLORED.value:
                    raise ValueError("Invalid edge " + f"({x1} {y1})" f"({x2} {y2}).")
                self.__grid[x1][y] = Graph.Status.OBSTACLE.value

            return

        slope = dy / dx
        if abs(slope) > 1:
            dy = sign(dy)
            slope = dy / slope
            xx = x1

            for y in range(y1, y2 + dy, dy):
                x = round(xx)
                if self.__grid[x][y] != Graph.Status.UNEXPLORED.value:
                    raise ValueError("Invalid edge " + f"({x1} {y1})" f"({x2} {y2}).")
                self.__grid[x][y] = Graph.Status.OBSTACLE.value

                xx += slope
        else:
            dx = sign(dx)
            slope = dx * slope
            yy = y1

            for x in range(x1, x2 + dx, dx):
                y = round(yy)
                if self.__grid[x][y] != Graph.Status.UNEXPLORED.value:
                    raise ValueError("Invalid edge " + f"({x1} {y1})" f"({x2} {y2})")
                self.__grid[x][y] = Graph.Status.OBSTACLE.value

                yy += slope

    def __dfs_polygon(self, x, y):
        cur = self.__grid[x][y]
        if cur == Graph.Status.OBSTACLE.value or cur == Graph.Status.UNUSED.value:
            return

        if cur != Graph.Status.UNEXPLORED.value:
            raise ValueError("Start or end point inside an obstacle.")

        self.__grid[x][y] = Graph.Status.UNUSED.value
        for dx, dy in self.__direction:
            self.__dfs_polygon(x + dx, y + dy)

    def __check_polygon(self, obs_vertices):
        cnt = len(obs_vertices)

        y_last, x_last = obs_vertices[-2:]
        if (
            not self.__bound_check(x_last, y_last)
            or self.__grid[x_last][y_last] != Graph.Status.UNEXPLORED.value
        ):
            raise ValueError("Obstacle edge overlapped with something.")

        self.__draw_edge(x_last, y_last, obs_vertices[1], obs_vertices[0])
        self.__grid[x_last][y_last] = Graph.Status.UNEXPLORED.value

        for i in range(2, cnt, 2):
            self.__draw_edge(
                obs_vertices[i - 1],
                obs_vertices[i - 2],
                obs_vertices[i + 1],
                obs_vertices[i],
            )

        avr_x = round(sum(obs_vertices[1::2]) / cnt * 2)
        avr_y = round(sum(obs_vertices[::2]) / cnt * 2)

        self.__dfs_polygon(avr_x, avr_y)

    # Hàm tạo: nhận 2 tham số là tên file input và tên thuật toán được sử dụng
    def __init__(self, input_path: str, algorithm: str = ""):
        with open(input_path, "r") as file_buffer:
            m, n = map(int, file_buffer.readline().split(","))
            self.__n, self.__m = n, m
            self.__algorithm = algorithm
            self.__map = pyplot.figure(figsize=(6, 6))
            # self.__map.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
            # self.__map.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

            self.__parent = np.array(
                [np.array([(i, j) for j in range(m + 2)]) for i in range(n + 2)]
            )

            self.__grid = np.array(
                [
                    np.array(
                        [
                            (
                                Graph.Status.WALL.value
                                if i == 0 or j == 0 or i == n + 1 or j == m + 1
                                else Graph.Status.UNEXPLORED.value
                            )
                            for j in range(m + 2)
                        ]
                    )
                    for i in range(n + 2)
                ]
            )
            self.__direction = np.array([(1, 0), (0, 1), (-1, 0), (0, -1)])

            colormap = colors.ListedColormap(
                [
                    "white",
                    "yellow",
                    "orange",
                    "grey",
                    "red",
                    "blue",
                    "green",
                    "purple",
                ]
            )

            start_y, start_x, end_y, end_x = map(int, file_buffer.readline().split(","))

            if not self.__bound_check(start_x, start_y):
                raise ValueError("Invalid start point.")

            if not self.__bound_check(end_x, end_y):
                raise ValueError("Invalid end point.")

            self.__grid[start_x][start_y] = Graph.Status.START.value
            self.__grid[end_x][end_y] = Graph.Status.GOAL.value

            self.__start = (start_x, start_y)
            self.__goal = (end_x, end_y)

            num_of_obs = int(file_buffer.readline())
            for _ in range(num_of_obs):
                obs_vertices = list(map(int, file_buffer.readline().split(",")))
                self.__check_polygon(obs_vertices)

            self.__im = pyplot.imshow(
                self.__grid,
                colormap,
                vmin=0,
                vmax=7,
                interpolation="none",
                extent=(0, self.__m + 2, self.__n + 2, 0),
            )
            pyplot.xticks(range(0, self.__m + 3))
            pyplot.yticks(range(0, self.__n + 3))
            pyplot.grid()
            self.__map.gca().invert_yaxis()
            self.__visited = 1
            self.__states = [self.__grid.copy()]

    def __animation_func(self, cur_frame: int):
        if cur_frame == 1:
            sleep(0.5)
        self.__im.set_array(self.__states[cur_frame])
        return [self.__im]

    def __output_animation(self):
        anim = animation.FuncAnimation(
            self.__map,
            self.__animation_func,
            len(self.__states),
            interval=10,  # in ms
            # blit=True,
        )

        pyplot.title(self.__algorithm)
        output_file = rf"{self.__algorithm}.gif"
        anim.save(output_file, writer="pillow")
        print(f"Animation saved to {output_file}.")
        pyplot.close()

    def __display(self):
        self.__visited += 1
        shorted_len = 0

        x, y = self.__goal
        while (x, y) != self.__start:
            shorted_len += 1
            self.__grid[x][y] = Graph.Status.PATH.value
            self.__states.append(self.__grid.copy())
            x, y = self.__parent[x][y]
        self.__grid[x][y] = Graph.Status.PATH.value
        self.__states.append(self.__grid.copy())

        print(f"Algorithm: {self.__algorithm}.")
        print(f"Path length: {shorted_len}.")
        print(f"Visited: {self.__visited} nodes.")

        self.__output_animation()

    # Hàm expand: nhận 1 tham số là cặp số (tuple) x, y chứa vị trí muốn expand. Hàm trả về 2 mảng: các vị trí đã được expand và các vị trí đã ở frontier.
    # Hàm có thể không trả gì nếu đã tìm thấy đích. Lúc đó, hàm này sẽ output ra kết quả.
    # Hàm throw exception nếu vị trí đó đã được expanded.
    # Hàm mặc định gắn parent của các đỉnh của mảng trả về đầu tiên là vị trí truyền vào tham số.

    # Hàm expand: không nhận tham số: khi đó hàm sẽ expand đỉnh đầu và vẫn trả về 2 mảng các vị trí đã được expand
    def expand(self, p: tuple | None = None) -> list[tuple] | None:
        if p is None or p == self.__start:
            x, y = self.__start
            if self.__grid[x][y] != Graph.Status.START.value:
                raise RuntimeError("Start point already expanded.")
            p = self.__start
        else:
            x, y = p
            if self.__grid[x][y] != Graph.Status.FRONTIER.value:
                raise RuntimeError("Expanding point not a frontier node.")
            self.__grid[x][y] = Graph.Status.EXPLORED.value

        x, y = p
        expanded = []
        frontier = []
        for dx, dy in self.__direction:
            new_x = x + dx
            new_y = y + dy
            cur = self.__grid[new_x][new_y]

            if cur == Graph.Status.GOAL.value:
                self.__parent[new_x][new_y] = p
                self.__display()
                return None

            if cur == Graph.Status.FRONTIER.value:
                frontier.append((new_x, new_y))

            if cur == Graph.Status.UNEXPLORED.value:
                self.__grid[new_x][new_y] = Graph.Status.FRONTIER.value
                self.__parent[new_x][new_y] = p
                expanded.append((new_x, new_y))

        self.__visited += len(expanded)
        self.__states.append(self.__grid.copy())
        return (expanded, frontier)

    # Hàm set_parent: nhận 2 tham số là vị trí cần thay đổi pos và giá trị thay đổi par. Khi đó, đỉnh trước pos sẽ được chỉnh thành par
    def set_parent(self, pos: tuple, parent: tuple) -> None:
        x, y = pos
        dx = abs(x - parent[0])
        dy = abs(y - parent[1])

        if (dx != 0 or dy != 1) and (dx != 1 or dy != 0):
            raise RuntimeError(f"{parent} is not a parent of {pos}.")

        if (
            self.__grid[x][y] != Graph.Status.EXPLORED.value
            and self.__grid[x][y] != Graph.Status.FRONTIER.value
        ):
            raise RuntimeError(f"{pos} has not been explored.")

        self.__parent[x][y] = parent

    # Hàm get_start: trả về điểm bắt đầu của đồ thị
    def get_start(self) -> tuple:
        return self.__start

    # Hàm get_goal: trả về điểm đích của đồ thị
    def get_goal(self) -> tuple:
        return self.__goal

    def is_explored(self, p: tuple) -> bool:
        return (
            p == self.__start or self.__grid[p[0]][p[1]] == Graph.Status.EXPLORED.value
        )

    # Hàm heuristic: nhận 1 tham số là cặp số (tuple) x, y muốn tìm giá trị heuristic, là khoảng cách Mahattan giữa điểm đó và điểm đích
    def hueristic(self, p: tuple) -> int:
        x, y = p
        end_x, end_y = self.__goal
        return abs(x - end_x) + abs(y - end_y)

    # Hàm give_up: không nhận tham số, chỉ sử dụng khi chắc chắn là không tồn tại đường đi
    def give_up(self) -> None:
        print(f"Algorithm: {self.__algorithm}.")
        print("No path found.")
        print(f"Visited: {self.__visited} nodes.")

        self.__output_animation()
