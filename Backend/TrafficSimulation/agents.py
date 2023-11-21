# Traffic Simulation Agents
# Definition for the agents used in the traffic simulation.

# Last Update: 20/Nov/2023
# Joaquín Badillo

from mesa import Agent
from enum import Enum

class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = 4
        self.steps_taken = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        
        # Checks which grid cells are empty
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        next_moves = [p for p,f in zip(possible_steps, freeSpaces) if f == True]
       
        next_move = self.random.choice(next_moves)

        # Now move:
        if self.random.random() < 0.1:
            self.model.grid.move_agent(self, next_move)
            self.steps_taken+=1

    def step(self):
        self.move()

class Destination(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

class Obstacle(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass  

class Road(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
    def step(self):
        pass

Color = Enum('Color', ['RED', 'GREEN'])
class Stoplight(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = Color.RED
        
    def step(self):
        pass