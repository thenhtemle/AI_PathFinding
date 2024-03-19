from enum import Enum
import numpy as np
from matplotlib import pyplot, colors
import matplotlib.animation as animation
from time import sleep
import heapq


class Graph:

    class Status(Enum):
        UNUSED = -1
        UNEXPLORED = 0
        WALL = 1
        OBSTACLE = 2
        START = 3
        GOAL = 4
        PATH = 5
        STOP = 6
        CUR_POS = 7

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
                    "grey",
                    "red",
                    "blue",
                    "green",
                    "purple",
                    "brown",
                    "orange",
                ]
            )

            line_tmp = file_buffer.readline().split(",")
            start_y, start_x, end_y, end_x = map(int, line_tmp[0:4])

            if not self.__bound_check(start_x, start_y):
                raise ValueError("Invalid start point.")

            if not self.__bound_check(end_x, end_y):
                raise ValueError("Invalid end point.")

            self.__grid[start_x][start_y] = Graph.Status.START.value
            self.__grid[end_x][end_y] = Graph.Status.GOAL.value

            self.__start = (start_x, start_y)
            self.__goal = (end_x, end_y)

            # Them diem don
            self.__stops = []
            i = 4
            while i < len(line_tmp):
                stop_y, stop_x = map(int, line_tmp[i : i + 2])
                if not self.__bound_check(stop_x, stop_y):
                    raise ValueError("Invalid stop point.")
                self.__grid[stop_x][stop_y] = Graph.Status.STOP.value
                self.__stops.append((stop_x, stop_y))
                i += 2

            self.num_of_obs = int(file_buffer.readline())
            for _ in range(self.num_of_obs):
                self.obs_vertices = list(map(int, file_buffer.readline().split(",")))
                self.__check_polygon(self.obs_vertices)

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
            self.__states = [self.__grid.copy()]

            output_path = input("Enter the name of the output file (no extension): ")
            self.__output_path = "output" if len(output_path) == 0 else output_path

    def __animation_func(self, cur_frame: int):
        if cur_frame == 1:
            sleep(0.5)
        self.__im.set_array(self.__states[cur_frame])
        return [self.__im]

    def output_animation(self):
        anim = animation.FuncAnimation(
            self.__map,
            self.__animation_func,
            len(self.__states),
            interval=10,  # in ms
            # blit=True,
        )

        pyplot.title(f"{self.__algorithm} with stop points.")
        output_file = rf"{self.__output_path}.gif"
        anim.save(output_file, writer="pillow")
        print(f"Animation saved to {output_file}.")
        pyplot.close()

    # Hàm get_start: trả về điểm bắt đầu của đồ thị
    def get_start(self) -> tuple:
        return self.__start

    # Hàm get_goal: trả về điểm đích của đồ thị
    def get_goal(self) -> tuple:
        return self.__goal

    # Hàm get_stops: trả về danh sách các điểm dừng của đồ thị
    def get_stops(self) -> list[tuple]:
        return self.__stops

    def add_state(self) -> None:
        self.__states.append(self.__grid.copy())

        for x, y in self.__stops:
            self.__grid[x][y] = Graph.Status.STOP.value
        x, y = self.__start
        self.__grid[x][y] = Graph.Status.START.value

    def set_path(self, p: tuple) -> None:
        x, y = p
        if (
            not self.__bound_check(x, y)
            or self.__grid[x][y] == Graph.Status.OBSTACLE.value
            or self.__grid[x][y] == Graph.Status.UNUSED.value
        ):
            raise RuntimeError(f"Point ({x} {y}) is inside an obstacle.")
        self.__grid[x][y] = Graph.Status.PATH.value

    def set_cur_pos(self, p: tuple) -> None:
        x, y = p
        if (
            not self.__bound_check(x, y)
            or self.__grid[x][y] == Graph.Status.OBSTACLE.value
            or self.__grid[x][y] == Graph.Status.UNUSED.value
        ):
            raise RuntimeError(f"Point ({x} {y}) is inside an obstacle.")
        self.__grid[x][y] = Graph.Status.CUR_POS.value

    def find_shortest_path(self, start: tuple, end: tuple) -> tuple | None:

        start_grid = self.__grid[start[0]][start[1]]
        end_grid = self.__grid[start[0]][start[1]]

        def check_valid(value: int) -> bool:
            return (
                value != Graph.Status.UNUSED.value
                and value != Graph.Status.OBSTACLE.value
                and value != Graph.Status.WALL.value
            )

        if not check_valid(start_grid):
            raise RuntimeError(f"Invalid start point {start}.")

        if not check_valid(end_grid):
            raise RuntimeError(f"Invalid start point {end}.")

        temp_grid = self.__grid.copy()

        def heuristic(p: tuple) -> int:
            return abs(p[0] - end[0]) + abs(p[1] - end[1])

        min_value_threshold = heuristic(start)
        wait_list = [(min_value_threshold, min_value_threshold, start, start)]
        parent = {start: start}

        def trace() -> tuple | None:
            nonlocal end
            path = [end]
            while end != start:
                end = parent[end]
                path.append(end)

            path.reverse()
            return (path, len(path) - 1)

        while len(wait_list) != 0:
            f, h, p, par = heapq.heappop(wait_list)
            x, y = p
            if temp_grid[x][y] == Graph.Status.UNUSED.value:
                continue

            temp_grid[x][y] = Graph.Status.UNUSED.value
            parent[p] = par
            min_value_threshold = max(min_value_threshold, f)

            g = f - h + 1
            dfs_stack = []
            for dx, dy in self.__direction:
                new_x = x + dx
                new_y = y + dy

                new_point = (new_x, new_y)
                if new_point == end:
                    parent[end] = p
                    return trace()

                if check_valid(temp_grid[new_x][new_y]):
                    dfs_stack.append((g, new_point, p))

            while len(dfs_stack) != 0:
                g, p, par = dfs_stack.pop()
                h = heuristic(p)

                if g + h > min_value_threshold:
                    heapq.heappush(wait_list, (g + h, h, p, par))
                    continue

                x, y = p
                if temp_grid[x][y] == Graph.Status.UNUSED.value:
                    continue

                temp_grid[x][y] = Graph.Status.UNUSED.value
                parent[p] = par

                for dx, dy in self.__direction:
                    new_x = x + dx
                    new_y = y + dy

                    new_point = (new_x, new_y)
                    if new_point == end:
                        parent[end] = p
                        return trace()

                    if check_valid(temp_grid[new_x][new_y]):
                        dfs_stack.append((g + 1, new_point, p))

        return None
