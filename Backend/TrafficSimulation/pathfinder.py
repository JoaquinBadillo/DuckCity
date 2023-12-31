# Pathfinder 🤖 
# Fine... I'll do it myself (╯°□°）╯︵ ┻━┻

# A* Pathfinding Algorithm Implementation
# Uses the model to determine valid neighbors

# Last Update: 21/Nov/2023
# Joaquín Badillo, Pablo Bolio

import heapq
from .agents import Road, Obstacle, Destination
from .utilities import Directions
from typing import Tuple, List, Callable

class GPS:
    def __init__(self, model):
        self.model = model

    def inside(self, x, y) -> bool:
        return 0 <= x < self.model.width and 0 <= y < self.model.height

    def valid(self, x, y, directions: Tuple[Tuple[int]], goal: Tuple[int]) -> bool:
        if not self.inside(x, y): return False
        
        cell = self.model.grid.get_cell_list_contents([(x, y)])

        destination = next(filter(lambda agent: type(agent) == Destination, cell), None)

        if destination is not None and destination.pos == goal: return True

        # To block a route (on recalculation) an agent can add temp obstacles
        obstacles = tuple(filter(lambda agent: type(agent) == Obstacle, cell))

        if len(obstacles) > 0: return False
        
        road = next(filter(lambda agent: type(agent) == Road, cell), None)

        if road is None: return False
        
        # Check if the direction of the road matches with direction of movement
        # Sidenote... although this trashy code is O(n^2), n is at most 2
        # Yes, we could use a set, but hashing might take longer with 2 elements
        return any(direction in road.directions for direction in directions)
    
    def get_neighbors(self, position, end) -> List[Tuple]:
        neighbors = []
        x, y = position

        # -- Straight Directions --

        # ↓
        if self.valid(x, y - 1, (Directions.DOWN,), end):
            neighbors.append((x, y - 1))
        
        # → 
        if self.valid(x + 1, y, (Directions.RIGHT,), end):
            neighbors.append((x + 1, y))

        # ↑
        if self.valid(x, y + 1, (Directions.UP,), end):
            neighbors.append((x, y + 1))
        
        # ←
        if self.valid(x - 1, y, (Directions.LEFT,), end):
            neighbors.append((x - 1, y))

        # -- Diagonals --

        # ↖ (Works for ↑ and ← roads) 
        if self.valid(x - 1, y + 1, (Directions.UP, Directions.LEFT), end):
            neighbors.append((x - 1, y + 1))

        # ↗ (Works for ↑ and → roads)
        if self.valid(x + 1, y + 1, (Directions.UP, Directions.RIGHT), end):
            neighbors.append((x + 1, y + 1))

        # ↘ (Works for ↓ and → roads)
        if self.valid(x + 1, y - 1, (Directions.DOWN, Directions.RIGHT), end):
            neighbors.append((x + 1, y - 1))

        # ↙ (Works for ↓ and ← roads)
        if self.valid(x - 1, y - 1, (Directions.DOWN, Directions.LEFT), end):
            neighbors.append((x - 1, y - 1))

        return neighbors

    # Avoid sqrt for performance
    def euclidean_distance(self, start: Tuple[int], end: Tuple[int]) -> float:
        return (start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2
        
    def chebychev_distance(self, start: Tuple[int], end: Tuple[int]) -> int:
        return max(abs(start[0] - end[0]), abs(start[1] - end[1]))

    def manhattan_distance(self, start: Tuple[int], end: Tuple[int]) -> int:
        return abs(start[0] - end[0]) + abs(start[1] - end[1])
    

    def astar(self, 
              start: Tuple[int], 
              end: Tuple[int],
              cost: Callable = None,
              heuristic: Callable = None) -> List[Tuple[int]]:
        
        # Default values
        if cost is None: cost = self.euclidean_distance
        if heuristic is None: heuristic = self.manhattan_distance

        pq = []
        heapq.heappush(pq, (0, start))

        came_from = dict()
        cost_so_far = dict()

        came_from[start] = None
        cost_so_far[start] = 0

        while len(pq) > 0:
            current = heapq.heappop(pq)[1]

            if current == end:
                break

            for neighbor in self.get_neighbors(current, end):
                new_cost = cost_so_far[current] + cost(current, neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, end)
                    heapq.heappush(pq, (priority, neighbor))
                    came_from[neighbor] = current

        # Manage impossible paths ᓚᘏᗢ
        if end not in came_from:
            return None

        path = []
        current = end

        while current != start:
            path.append(current)
            current = came_from[current]

        return path