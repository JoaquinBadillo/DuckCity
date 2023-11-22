# Traffic Simulation Agents
# Definition for the agents used in the traffic simulation.

# Last Update: 20/Nov/2023
# Joaquín Badillo

from mesa import Agent

from utilities import (
    Directions,
    Colors
)

from typing import List

class Car(Agent):
    def __init__(self, unique_id, model, destination) -> None:
        super().__init__(unique_id, model)
        self.steps_taken = 0
        self.destination = destination
        self.route = self.model.finder.astar(self.pos, self.destination)
        
        self.turn = None

        self.model = model
        self.arrived = False

    def action(self) -> None:
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
            if stoplight.state == Colors.RED or stoplight.state == Colors.YELLOW:
                self.wait()
                return

        # Turn directionals if taking a turn in at most 5 steps
        if self.turn is None:
            limit = 5
            
            for x, y in self.route:
                if limit == 0: break

                if x != self.pos[0]:
                    if x < self.pos[0]:
                        self.turn_directional(Directions.LEFT)
                    else:
                        self.turn_directional(Directions.RIGHT)
                    break
                elif y != self.pos[1]:
                    if y < self.pos[1]:
                        self.turn_directional(Directions.UP)
                    else:
                        self.turn_directional(Directions.DOWN)
                    break

                limit -= 1


        neighbors = self.model.grid.get_neighborhood(self.pos, 
                                                     moore=False, 
                                                     include_center=False)

        # -- Decision Making --
    
        pass

    def move(self, pos) -> None:
        self.model.grid.move_agent(self, pos)

    def calculate_route(self, blockages: List[int] = None) -> None:
        temp = []

        # Use custom blockages for A* to avoid clustered routes on recalculation
        if blockages is not None:
            for idx, position in enumerate(blockages):
                agent = Obstacle(f"temp{idx}", self.model)
                temp.append(agent)
                self.model.grid.place_agent(agent, position)

        path = self.model.finder.astar(self.pos, self.destination)
        
        if self.route is None:
            self.route = path
        
        # Toleration for a 30% increase in route length
        # TODO - May change this to a percentage based on behavioral states
        elif len(path) < 1.3 * len(self.route):
            self.route = path

        # Temp Cleanup
        for agent in temp:
            self.model.grid.remove_agent(agent)
    
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
    def __init__(self, unique_id, model, direction) -> None:
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self) -> None:
        pass

class Stoplight(Agent):
    def __init__(self, unique_id, model, state) -> None:
        super().__init__(unique_id, model)
        self.state = state
        self.counter = 0
    
    def change_state(self) -> None:
        self.state = Colors(self.state.value % len(Colors) + 1)

    def step(self) -> None:
        # TODO - Toggle state using counter
        pass