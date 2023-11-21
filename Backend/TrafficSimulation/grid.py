# Custom Grid For Pathfinding Library
# Implements some functions from the grid interface for the pathfinding library
# This implementation uses the mesa grid to determine if a node is walkable or 
# not

# Last Update: 21/Nov/2023
# Joaquín Badillo

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.node import GridNode
from pathfinding.core.util import build_nodes, SQRT2

from agents import (
    Car,
    Destination,
    Obstacle,
    Road,
    Stoplight,
    Directions,
    Colors
)

from typing import List

class Grid:
    def __init__(self, model=None):
        self.model = model
        self.width = model.width
        self.height = model.height

        self.nodes = build_nodes(
            self.width, self.height
        )

    def node(self, x, y) -> GridNode:
        return self.nodes[y][x]

    def inside(self, x, y) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def walkable(self, x, y, direction) -> bool:
        if not self.inside(x, y):
            return False

        cell = self.model.grid.get_cell_list_contents([(x, y)])    
        road = next(filter(lambda agent: type(agent) == Road, cell), None)

        if road is None or road.direction != direction:
            return False

        cars = tuple(filter(lambda agent: type(agent) == Car, cell))

        return len(cars) == 0

    def calc_cost(self, node_a, node_b, weighted=False):
        if node_b.x - node_a.x == 0 or node_b.y - node_a.y == 0:
            ng = 1
        else:
            ng = SQRT2

        if weighted:
            ng *= node_b.weight

        return node_a.g + ng

    def neighbors(
        self, node: GridNode,
        diagonal_movement: DiagonalMovement = DiagonalMovement.never
    ) -> List[GridNode]:
        x = node.x
        y = node.y
        neighbors = []
        s0 = d0 = s1 = d1 = s2 = d2 = s3 = d3 = False

        # ↑
        if y != 0:
            if self.walkable(x, y - 1, Directions.DOWN):
                neighbors.append(self.nodes[y - 1][x])
                s0 = True
        
        # →
        if x < self.width - 1:
            if self.walkable(x + 1, y, Directions.RIGHT):
                neighbors.append(self.nodes[y][x + 1])
                s1 = True

        if x == self.width - 1 and self.passable_left_right_border:
            if self.walkable(0, y):
                neighbors.append(self.nodes[y][0])
                s1 = True
        else:
            if self.walkable(x + 1, y):
                neighbors.append(self.nodes[y][x + 1])
                s1 = True
        # ↓
        if y == self.height - 1 and self.passable_up_down_border:
            if self.walkable(x, 0):
                neighbors.append(self.nodes[0][x])
                s2 = True
        else:
            if self.walkable(x, y + 1):
                neighbors.append(self.nodes[y + 1][x])
                s2 = True
        # ←
        if x == 0 and self.passable_left_right_border:
            if self.walkable(self.width - 1, y):
                neighbors.append(self.nodes[y][self.width - 1])
                s3 = True
        else:
            if self.walkable(x - 1, y):
                neighbors.append(self.nodes[y][x - 1])
                s3 = True

        # check for connections to other grids
        if node.connections:
            neighbors.extend(node.connections)

        if diagonal_movement == DiagonalMovement.never:
            return neighbors

        if diagonal_movement == DiagonalMovement.only_when_no_obstacle:
            d0 = s3 and s0
            d1 = s0 and s1
            d2 = s1 and s2
            d3 = s2 and s3
        elif diagonal_movement == DiagonalMovement.if_at_most_one_obstacle:
            d0 = s3 or s0
            d1 = s0 or s1
            d2 = s1 or s2
            d3 = s2 or s3
        elif diagonal_movement == DiagonalMovement.always:
            d0 = d1 = d2 = d3 = True

        # ↖
        if d0 and self.walkable(x - 1, y - 1):
            neighbors.append(self.nodes[y - 1][x - 1])

        # ↗
        if d1 and self.walkable(x + 1, y - 1):
            neighbors.append(self.nodes[y - 1][x + 1])

        # ↘
        if d2 and self.walkable(x + 1, y + 1):
            neighbors.append(self.nodes[y + 1][x + 1])

        # ↙
        if d3 and self.walkable(x - 1, y + 1):
            neighbors.append(self.nodes[y + 1][x - 1])

        return neighbors

    def cleanup(self):
        for y_nodes in self.nodes:
            for node in y_nodes:
                node.cleanup()

    def grid_str(self, path=None, start=None, end=None,
                 border=True, start_chr='s', end_chr='e',
                 path_chr='x', empty_chr=' ', block_chr='#',
                 show_weight=False) -> str:
        """
        create a printable string from the grid using ASCII characters

        :param path: list of nodes that show the path
        :param start: start node
        :param end: end node
        :param border: create a border around the grid
        :param start_chr: character for the start (default "s")
        :param end_chr: character for the destination (default "e")
        :param path_chr: character to show the path (default "x")
        :param empty_chr: character for empty fields (default " ")
        :param block_chr: character for blocking elements (default "#")
        :param show_weight: instead of empty_chr show the cost of each empty
                            field (shows a + if the value of weight is > 10)
        :return:
        """
        # create a dict as lookup-table for the path by string for performance
        path_cache = {}
        if path:
            for node in path:
                is_gn = isinstance(node, GridNode)
                x, y = (node.x, node.y) if is_gn else node[:2]
                path_cache[f'{x}_{y}'] = True

        # create the output string
        data = ''
        if border:
            data = f'+{"-" * len(self.nodes[0])}+'
        for y in range(len(self.nodes)):
            line = ''
            for x in range(len(self.nodes[y])):
                node = self.nodes[y][x]
                if node == start:
                    line += start_chr
                elif node == end:
                    line += end_chr
                elif path and (f'{x}_{y}' in path_cache):
                    line += path_chr
                elif node.walkable:
                    # empty field
                    weight = str(node.weight) if node.weight < 10 else '+'
                    line += weight if show_weight else empty_chr
                else:
                    line += block_chr  # blocked field
            if border:
                line = f'|{line}|'
            if data:
                data += '\n'
            data += line
        if border:
            data += f'\n+{"-" * len(self.nodes[0])}+'
        return data

    def __repr__(self):
        """
        return a human readable representation
        """
        return f"<{self.__class__.__name__} " \
            f"width={self.width} height={self.height}>"