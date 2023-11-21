# Traffic Simulation Model
# Defines a Multigrid model for the traffic simulation.

# The grid will be initialized with roads and stoplights using a document. Also,
# a given number of cars will be initialized, but after each iteration more cars
# will be added to the grid.

# Last Update: 20/Nov/2023
# Joaquín Badillo

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from agents import Car, Destination, Obstacle, Road, Stoplight

class TrafficModel(Model):
    def __init__(self,
                 num_agents=10,
                 width=50,
                 height=50):
        super().__init__()

        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        # Stats
        self.num_steps = 0
        self.num_agents = num_agents
        self.num_arrivals = 0
    
        # Initialize agents
        # TODO - Parse document

        # TODO - Add agents to schedule

        self.running = True

    def step(self):
        self.schedule.step()
        self.num_steps += 1
        
        # TODO - Add more cars (if possible)
        self.num_agents += 4