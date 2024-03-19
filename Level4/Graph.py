from enum import Enum
import numpy as np
from matplotlib import pyplot, colors
import matplotlib.animation as animation


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

    def __move_point(self, x: int, y: int, dx: int, dy: int):

        def sign(x: int) -> int:
            return 1 if x > 0 else -1

        if self.__other_grid[x + dx][y + dy] > 0:
            raise ValueError("Invalid movement.")
        self.__other_grid[x + dx][y + dy] = Graph.Status.OBSTACLE.value

        if dy == 0:
            sign_x = sign(dx)
            for new_x in range(x, x + dx + sign_x, sign_x):
                cur = self.__grid[new_x][y]
                if (
                    cur == Graph.Status.START.value
                    or cur == Graph.Status.GOAL.value
                    or cur == Graph.Status.WALL.value
                ):
                    raise ValueError("Invalid movement.")
                self.__movement_matrix[new_x][y] = True

            return

        if dx == 0:
            sign_y = sign(dy)
            for new_y in range(y, y + dy + sign_y, sign_y):
                cur = self.__grid[x][new_y]
                if (
                    cur == Graph.Status.START.value
                    or cur == Graph.Status.GOAL.value
                    or cur == Graph.Status.WALL.value
                ):
                    raise ValueError("Invalid movement.")
                self.__movement_matrix[x][new_y] = True

            return

        slope = dy / dx
        if abs(slope) > 1:
            sdy = sign(dy)
            slope = dy / slope
            xx = x

            for new_y in range(y, y + dy + sdy, sdy):
                x = round(xx)
                cur = self.__grid[x][new_y]
                if (
                    cur == Graph.Status.START.value
                    or cur == Graph.Status.GOAL.value
                    or cur == Graph.Status.WALL.value
                ):
                    raise ValueError("Invalid movement.")
                self.__movement_matrix[x][new_y] = True

                xx += slope
        else:
            sdx = sign(dx)
            slope = dx * slope
            yy = y

            for new_x in range(x, x + dx + sdx, sdx):
                y = round(yy)
                cur = self.__grid[new_x][y]
                if (
                    cur == Graph.Status.START.value
                    or cur == Graph.Status.GOAL.value
                    or cur == Graph.Status.WALL.value
                ):
                    raise ValueError("Invalid movement.")
                self.__movement_matrix[new_x][y] = True

                yy += slope

    def __draw_edge(
        self, x1: int, y1: int, x2: int, y2: int, move_x: int, move_y: int
    ) -> None:

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
                self.__move_point(x, y1, move_x, move_y)

            return

        if dx == 0:
            sign_y = sign(dy)
            for y in range(y1, y2 + sign_y, sign_y):
                if self.__grid[x1][y] != Graph.Status.UNEXPLORED.value:
                    raise ValueError("Invalid edge " + f"({x1} {y1})" f"({x2} {y2}).")
                self.__grid[x1][y] = Graph.Status.OBSTACLE.value
                self.__move_point(x1, y, move_x, move_y)

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
                self.__move_point(x, y, move_x, move_y)

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
                self.__move_point(x, y, move_x, move_y)

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

    def __check_polygon(self, obs_vertices, movement):
        cnt = len(obs_vertices)
        dy, dx = movement

        y_last, x_last = obs_vertices[-2:]
        if (
            not self.__bound_check(x_last, y_last)
            or self.__grid[x_last][y_last] != Graph.Status.UNEXPLORED.value
        ):
            raise ValueError("Obstacle edge overlapped with something.")

        self.__draw_edge(x_last, y_last, obs_vertices[1], obs_vertices[0], dx, dy)
        self.__grid[x_last][y_last] = Graph.Status.UNEXPLORED.value
        self.__other_grid[x_last + dx][y_last + dy] = Graph.Status.UNEXPLORED.value

        for i in range(2, cnt, 2):
            self.__other_grid[obs_vertices[i - 1] + dx][
                obs_vertices[i - 2] + dy
            ] = Graph.Status.UNEXPLORED.value
            self.__draw_edge(
                obs_vertices[i - 1],
                obs_vertices[i - 2],
                obs_vertices[i + 1],
                obs_vertices[i],
                dx,
                dy,
            )

        avr_x = round(sum(obs_vertices[1::2]) / cnt * 2)
        avr_y = round(sum(obs_vertices[::2]) / cnt * 2)

        self.__dfs_polygon(avr_x, avr_y)

    # Hàm tạo: nhận 2 tham số là tên file input và tên thuật toán được sử dụng
    def __init__(self, input_path: str):
        with open(input_path, "r") as file_buffer:
            m, n = map(int, file_buffer.readline().split(","))
            self.__n, self.__m = n, m

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
            self.__movement_matrix = np.array(
                [np.array([(False) for j in range(m + 2)]) for i in range(n + 2)]
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
            self.__other_grid = self.__grid.copy()

            self.__start = (start_x, start_y)
            self.__goal = (end_x, end_y)

            num_of_obs = int(file_buffer.readline())
            obs_vertices = []
            for _ in range(num_of_obs):
                obs_vertices.append(list(map(int, file_buffer.readline().split(","))))

            movements = []
            for _ in range(num_of_obs):
                movements.append(tuple(map(int, file_buffer.readline().split(","))))

            for vertices, movement in zip(obs_vertices, movements):
                self.__check_polygon(vertices, movement)

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
            self.__frontier = 0
            self.__shortest_path = 1
            self.__states = [self.__grid.copy()]

            output_path = input("Enter the name of the output file (no extension): ")
            self.__output_path = (
                "Moving obstacle" if len(output_path) == 0 else output_path
            )

    def __animation_func(self, cur_frame: int):
        self.__im.set_array(self.__states[cur_frame])
        return [self.__im]

    def __output_animation(self):
        anim = animation.FuncAnimation(
            self.__map,
            self.__animation_func,
            len(self.__states),
            interval=250,  # in ms
            # blit=True,
        )

        pyplot.title("Moving obstacles.")
        output_file = rf"{self.__output_path}.gif"
        anim.save(output_file, writer="pillow")
        print(f"Animation saved to {output_file}.")
        pyplot.close()

    def __display(self):
        shorted_len = self.__shortest_path

        x, y = self.__goal
        while (x, y) != self.__start:
            self.__grid[x][y] = Graph.Status.PATH.value
            self.__other_grid[x][y] = Graph.Status.PATH.value

            if shorted_len & 1 == 0:
                self.__states.append(self.__grid.copy())
            else:
                self.__states.append(self.__other_grid.copy())

            shorted_len -= 1
            x, y = self.__parent[x][y]

        self.__grid[x][y] = Graph.Status.PATH.value
        self.__states.append(self.__grid.copy())

        print(f"BFS with moving obstacles.")
        print(f"Path length: {self.__shortest_path}.")
        print(
            f"Visited: {self.__visited + 1} nodes ({self.__visited - self.__frontier} opened nodes, {self.__frontier} frontiers)."
        )

        self.__output_animation()

    def run(self):
        x, y = self.__start
        frontier = []
        discard = []

        for dx, dy in self.__direction:
            new_x = x + dx
            new_y = y + dy

            if self.__other_grid[new_x][new_y] == Graph.Status.OBSTACLE.value:
                pass

            self.__parent[new_x][new_y] = self.__start
            if self.__other_grid[new_x][new_y] == Graph.Status.GOAL.value:
                for f_x, f_y in frontier:
                    self.__grid[f_x][f_y] = Graph.Status.FRONTIER.value
                self.__frontier = len(frontier)
                self.__display()
                return

            self.__other_grid[new_x][new_y] = Graph.Status.FRONTIER.value

            if self.__movement_matrix[new_x][new_y]:
                discard.append((new_x, new_y))
            else:
                frontier.append((new_x, new_y))

        self.__states.append(self.__other_grid.copy())

        self.__frontier = len(frontier)
        self.__visited += len(discard)
        while len(frontier) != 0:
            new_frontier = []
            self.__frontier -= 1
            self.__shortest_path += 1

            if self.__shortest_path & 1 == 0:
                for x, y in discard:
                    self.__other_grid[x][y] = Graph.Status.UNEXPLORED.value
                discard.clear()

                for x, y in frontier:
                    self.__grid[x][y] = Graph.Status.EXPLORED.value
                    self.__other_grid[x][y] = Graph.Status.EXPLORED.value

                    for dx, dy in self.__direction:
                        new_x = x + dx
                        new_y = y + dy

                        if self.__grid[new_x][new_y] == Graph.Status.GOAL.value:
                            self.__parent[new_x][new_y] = (x, y)
                            for f_x, f_y in frontier:
                                self.__grid[f_x][f_y] = Graph.Status.FRONTIER.value
                            self.__display()
                            return

                        if self.__grid[new_x][new_y] == Graph.Status.OBSTACLE.value:
                            pass

                        if self.__grid[new_x][new_y] == Graph.Status.UNEXPLORED.value:
                            self.__visited += 1
                            self.__grid[new_x][new_y] = Graph.Status.FRONTIER.value

                            if self.__movement_matrix[new_x][new_y]:
                                discard.append((new_x, new_y))
                            else:
                                new_frontier.append((new_x, new_y))
                                self.__parent[new_x][new_y] = (x, y)

                self.__states.append(self.__grid.copy())

            else:
                for x, y in discard:
                    self.__grid[x][y] = Graph.Status.UNEXPLORED.value
                discard.clear()

                for x, y in frontier:
                    self.__grid[x][y] = Graph.Status.EXPLORED.value
                    self.__other_grid[x][y] = Graph.Status.EXPLORED.value

                    for dx, dy in self.__direction:
                        new_x = x + dx
                        new_y = y + dy

                        if self.__other_grid[new_x][new_y] == Graph.Status.GOAL.value:
                            self.__parent[new_x][new_y] = (x, y)
                            for f_x, f_y in frontier:
                                self.__other_grid[f_x][
                                    f_y
                                ] = Graph.Status.FRONTIER.value
                            self.__display()
                            return

                        if (
                            self.__other_grid[new_x][new_y]
                            == Graph.Status.OBSTACLE.value
                        ):
                            pass

                        if (
                            self.__other_grid[new_x][new_y]
                            == Graph.Status.UNEXPLORED.value
                        ):
                            self.__visited += 1
                            self.__other_grid[new_x][
                                new_y
                            ] = Graph.Status.FRONTIER.value

                            if self.__movement_matrix[new_x][new_y]:
                                discard.append((new_x, new_y))
                            else:
                                new_frontier.append((new_x, new_y))
                                self.__parent[new_x][new_y] = (x, y)

                self.__states.append(self.__other_grid.copy())

            frontier = new_frontier
            self.__frontier = len(frontier)
            self.__visited += len(discard)

        self.__give_up()

    # Hàm give_up: không nhận tham số, chỉ sử dụng khi chắc chắn là không tồn tại đường đi
    def __give_up(self) -> None:
        print(f"BFS with moving obstacles.")
        print("No path found.")
        print(f"Opened: {self.__visited} nodes.")

        self.__output_animation()
