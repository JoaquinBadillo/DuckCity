# Traffic Simulation Agents
# Definition for the agents used in the traffic simulation.

# Last Update: 20/Nov/2023
# Joaquín Badillo

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

        self.model = model
        self.arrived = False

    def action(self) -> None:
        if len(self.route) == 0: return

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
                self.wait()
                return

        # TODO - Turn directionals if taking a turn in at most 5 steps

        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                     moore=False, 
                                                     include_center=False)

        # -- Decision Making --
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
            self.wait()
            return

        self.move(pos)

        pass

    def move(self, pos) -> None:
        self.model.grid.move_agent(self, pos)
        if pos == self.destination: self.model.arrived_agents.append(self)

    def calculate_route(self, neighborhood = None) -> None:    
        obstacles = set(
            agent.pos for agent in 
            self.model.grid.get_cell_list_contents(neighborhood) 
            if isinstance(agent, Car) or isinstance(agent, Stoplight)
        ) if neighborhood is not None else set()


        def cost(start, neighbor, obstacles = obstacles) -> int:
            return 4 if neighbor in obstacles else (start[0] - neighbor[0]) ** 2 + (start[1] - neighbor[1]) ** 2

        path = self.model.gps.astar(self.pos, self.destination, cost=cost)
        
        if self.route is None:
            self.route = path
        
        # Toleration for a 30% increase in route length
        # TODO - May change this to a percentage based on behavioral states
        elif len(path) < 1.3 * len(self.route):
            self.route = path

    
    def turn_directional(self, direction) -> None:
        self.turn = direction
        pass

    def wait(self) -> None:
        # TODO - May change some state variables (tolerance meter or something)...
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