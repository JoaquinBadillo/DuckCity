# Traffic Simulation Agents
# Definition for the agents used in the traffic simulation.

# Last Update: 20/Nov/2023
# Joaquín Badillo

from mesa import Agent
from enum import Enum

# Road Directions
Directions = Enum('Directions', ['UP', 'RIGHT', 'LEFT', 'DOWN'])

# Stoplight Colors
Colors = Enum('Colors', ['GREEN', 'YELLOW', 'RED'])

class Car(Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.steps_taken = 0

    def move(self) -> None:
        pass

    def calculate_route(self) -> None:
        pass
    
    def turn_sidelight(self) -> None:
        pass

    def wait(self) -> None:
        pass

    def step(self) -> None:
        self.move()

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
    def __init__(self, unique_id, model, state, timer) -> None:
        super().__init__(unique_id, model)
        self.state = state
        self.timer = timer
        self.counter = 0
    
    def change_state(self) -> None:
        self.state = Colors(self.state.value % len(Colors) + 1)

    def step(self) -> None:
        # TODO - Toggle state using counter
        if self.state == Colors.GREEN and self.counter == self.timer - 2:
            self.change_state(self)
        elif self.state == Colors.YELLOW and self.counter == self.timer:
            self.change_state(self)
            self.counter = 0
        elif self.state == Colors.RED and self.counter == self.timer:
            self.change_state(self)
            self.counter = 0
        pass