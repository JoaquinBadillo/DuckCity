# Traffic Simulation Agents
# Definition for the agents used in the traffic simulation.

# Last Update: 20/Nov/2023
# Joaquín Badillo, Pablo Bolio

from mesa import Agent

from .utilities import (
    Directions,
    Colors
)

from typing import List, Tuple

class Car(Agent):
    def __init__(self, unique_id, model, destination) -> None:
        super().__init__(unique_id, model)
        self.steps_taken = 0
        self.destination = destination
        self.route = []
        
        self.turn = None

        self.initial_patience = self.random.randint(1, 5)
        self.patience = self.initial_patience
        self.threshold = self.random.randint(-6, -4)

        self.model = model
        self.arrived = False

    def action(self) -> None:
        if len(self.route) == 0: 
            return

        # -- State and Sensoring --
        
        # Stoplight (Currently sensed only in the same cell)
        stoplight = next(
            filter(
                lambda x: type(x) == Stoplight, 
                self.model.grid.get_cell_list_contents([self.pos])
            ), 
            None
        )
        
        if stoplight is not None:
            if stoplight.state == Colors.RED:
                self.wait(remove_patience=False)
                return

        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                     moore=False, 
                                                     include_center=False)

        # -- Decision Making --
        
        # Try to follow route
        moved = self.follow_route()
        
        if moved: return

        x, y = self.route[-1]
        
        # Only recalculates route if the car is not taking a turn
        if x != self.pos[0] and y != self.pos[1]:
            if self.patience > 0:
                self.wait()
                return
        
        # Martyr
        if self.patience <= self.threshold:
            neighs = self.model.gps.get_neighbors(self.pos, self.destination)
            free = [cell for cell in neighs 
                    if not any(
                        True for x in self.model.grid.get_cell_list_contents([cell]) 
                        if isinstance(x, Car)
                    )]
            if len(free) > 0:
                self.move(self.random.choice(free), resotre_patience=False)
                self.calculate_route(neighbors)
                return

        updated = self.calculate_route(neighbors)
        
        if not updated: 
            self.wait()
            return
        
        moved = self.follow_route()

        if not moved: 
            self.wait()
            return

    def follow_route(self) -> bool:
        pos = self.route.pop()

        car = next(
            filter(
                lambda x: type(x) == Car, 
                self.model.grid.get_cell_list_contents([pos])
            ), 
            None
        )

        if car is not None:
            self.route.append(pos)
            return False

        self.move(pos)
        return True

    def move(self, pos, resotre_patience = True) -> None:
        if resotre_patience:
            self.patience = self.initial_patience

        self.model.grid.move_agent(self, pos)
        if pos == self.destination: 
            self.model.arrived_agents.append(self)
            self.arrived = True

    def calculate_route(self, neighborhood = None) -> bool:
        obstacles = set(
            agent.pos for agent in 
            self.model.grid.get_cell_list_contents(neighborhood) 
            if isinstance(agent, Car)
        ) if neighborhood is not None else set()


        def cost(start, neighbor, obstacles = obstacles) -> int:
            neighbor_cost = 4 if self.patience >= 0 else 2**(-self.patience)
            return neighbor_cost if neighbor in obstacles else self.model.gps.euclidean_distance(start, neighbor)

        path = self.model.gps.astar(self.pos, self.destination, cost=cost)
        tolerance = 1.3 * len(self.route)

        if self.patience < 0:
            tolerance = self.model.width * self.model.height + 2**(-self.patience)

        if path is None: return False

        elif self.route is None:
            self.route = path
         
        elif len(path) < tolerance:
            self.route = path

        return True
    
    def turn_directional(self, direction) -> None:
        self.turn = direction
        pass

    def wait(self, remove_patience = True) -> None:
        if remove_patience:
            self.patience -= 1
        return

    def step(self) -> None:
        if self.arrived: return
        self.action()

class Destination(Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)

    def step(self) -> None:
        pass

class Obstacle(Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)

    def step(self) -> None:
        pass  


class Road(Agent):
    def __init__(self, unique_id, model, directions) -> None:
        super().__init__(unique_id, model)
        self.directions = directions

    def step(self) -> None:
        pass

class Stoplight(Agent):
    def __init__(self, unique_id, model, state, timer) -> None:
        super().__init__(unique_id, model)
        self.state = state
        self.timer = timer
        self.count = 0
    
    def change_state(self) -> None:
        self.state = Colors(self.state.value % len(Colors) + 1)

    def step(self) -> None:
        self.count = (self.count + 1) % self.timer
        if self.count == 0:
            self.change_state()
        pass