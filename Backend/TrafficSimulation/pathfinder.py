# Pathfinder 🤖 
# Fine... I'll do it myself (╯°□°）╯︵ ┻━┻

# A* Pathfinding Algorithm Implementation
# Uses the model to determine valid neighbors

# Last Update: 21/Nov/2023
# Joaquín Badillo

import heapq
from mesa.model import Model
from agents import Road, Obstacle
from utilities import Directions
from typing import Tuple, List, Callable

class AStar:
    def __init__(self, model: Model):
        self.model = model

    def inside(self, x, y) -> bool:
        return 0 <= x < self.model.width and 0 <= y < self.model.height

    def valid(self, x, y, directions) -> bool:
        if not self.inside(x, y):
            return False

        cell = self.model.grid.get_cell_list_contents([(x, y)])

        # To block a route (on recalculation) an agent can add temp obstacles
        obstacles = tuple(filter(lambda agent: type(agent) == Obstacle, cell))

        if len(obstacles) > 0:
            return False
        
        road = next(filter(lambda agent: type(agent) == Road, cell), None)

        if road is None:
            return False
        
        if road.direction not in directions:
            return False 

        return True
    
    def get_neighbors(self, position) -> List[Tuple]:
        cell = self.model.grid.get_cell_list_contents([position])
        road = next(filter(lambda agent: type(agent) == Road, cell), None)

        # Road should never be None tho, but hey we avoid a runtime error
        if road is None:
            return []

        direction = road.direction

        neighbors = []
        x, y = position

        # -- Straight Directions --

        # ↓
        if self.valid(x, y - 1, tuple(Directions.DOWN)):
            neighbors.append((x, y - 1))
        
        # → 
        if self.valid(x + 1, y, tuple(Directions.RIGHT)):
            neighbors.append((x + 1, y))

        # ↑
        if self.valid(x, y + 1, tuple(Directions.UP)):
            neighbors.append((x, y + 1))
        
        # ←
        if self.valid(self.width - 1, tuple(Directions.LEFT)):
            neighbors.append((x - 1, y))

        # -- Diagonals --

        # ↖ (Works for ↑ and ← roads) 
        if self.valid(x - 1, y + 1, tuple(Directions.UP, Directions.LEFT)):
            neighbors.append((x - 1, y + 1))

        # ↗ (Works for ↑ and → roads)
        if self.valid(x + 1, y + 1, tuple(Directions.UP, Directions.RIGHT)):
            neighbors.append((x + 1, y + 1))

        # ↘ (Works for ↓ and → roads)
        if self.valid(x + 1, y - 1, tuple(Directions.DOWN, Directions.RIGHT)):
            neighbors.append((x + 1, y - 1))

        # ↙ (Works for ↓ and ← roads)
        if self.valid(x - 1, y - 1, tuple(Directions.DOWN, Directions.LEFT)):
            neighbors.append((x - 1, y - 1))

        return neighbors

    def euclidean_distance(self, start: Tuple[int], end: Tuple[int]) -> float:
        return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5
        
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
        
        pq = heapq.PriorityQueue()
        pq.put((0, start))

        came_from = dict()
        cost_so_far = dict()

        came_from[start] = None
        cost_so_far[start] = 0

        while not pq.empty():
            current = heapq.heappop(pq)[1]

            if current == end:
                break

            for neighbor in self.get_neighbors(current):
                new_cost = cost_so_far[current] + cost(current, neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, end)
                    heapq.heappush(pq, (priority, neighbor))
                    came_from[neighbor] = current
        
        # Manage impossible paths ᓚᘏᗢ
        if end not in came_from:
            return [] 

        path = []
        current = end

        while current != start:
            path.append(current)
            current = came_from[current]

        path.reverse()

        return path






