# Traffic Simulation Model
# Defines a Multigrid model for the traffic simulation.

# The grid will be initialized with roads and stoplights using a document. Also,
# a given number of cars will be initialized, but after each iteration more cars
# will be added to the grid.

# Last Update: 20/Nov/2023
# Joaquín Badillo, Pablo Bolio

import logging
import sys
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from .agents import (
    Car,
    Destination,
    Obstacle,
    Road,
    Stoplight,
    Directions,
    Colors
)
import json

import os

logger = logging.getLogger("app.sub")
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(name)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class TrafficModel(Model):
    def __init__(self,
                 num_agents=10,
                 width=50,
                 height=50):
        super().__init__()

        logger.info("HI")
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        # Stats
        self.num_steps = 0
        self.num_agents = num_agents
        self.agent_id = 1
        self.added_agents = 0
        self.num_arrivals = 0
        self.traffic_lights = []
    
        # Initialize agents
        # TODO - Parse document
         
        dataDictionary = json.load(open(f"{os.getcwd()}/city_files/mapDictionary.json"))

        with open(f'{os.getcwd()}/city_files/2021_base2.txt') as city:
            lines = city.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

            # temporal
            down_counter = 0
            up_counter = 0
            right_counter = 0
            left_counter = 0
            up_left_counter = 0
            up_right_counter = 0
            down_left_counter = 0
            down_right_counter = 0

            # Goes through each character in the map file and creates the 
            # corresponding agent.
            # For double directions we used {} and []
            # Curly brackets are up diagonals and brackets are down diagonals
            for r, row in enumerate(lines):
                for c, col in enumerate(row):
                    if col in "v":
                        agent = Road(f"r_{r*self.width+c}", self, (Directions.DOWN,))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in "^":
                        agent = Road(f"r_{r*self.width+c}", self, (Directions.UP,))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ">":
                        agent = Road(f"r_{r*self.width+c}", self, (Directions.RIGHT,))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in "<":
                        agent = Road(f"r_{r*self.width+c}", self, (Directions.LEFT,))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in "{":
                        agent = Road(f"r_{r*self.width+c}", self, (Directions.UP, Directions.LEFT))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in "}":
                        agent = Road(f"r_{r*self.width+c}", self, (Directions.UP, Directions.RIGHT))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in "[":
                        agent = Road(f"r_{r*self.width+c}", self, (Directions.DOWN, Directions.LEFT,))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in "]":
                        agent = Road(f"r_{r*self.width+c}", self, (Directions.DOWN, Directions.RIGHT,))
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col in ["S", "s"]:
                        agent = Stoplight(f"tl_{r*self.width+c}", self, Colors.GREEN, int(dataDictionary[col]))
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.schedule.add(agent)
                        self.traffic_lights.append(agent)
                        
                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

        self.running = True

    def step(self):
        self.schedule.step()
        self.num_steps += 1
        
        # TODO - Add more cars (if possible)
        for i in range(4):
            if self.num_steps % 10 == 0 and self.grid.is_cell_empty(0,0):
                self.grid.place_agent(Car(f"car_{self.agent_id}", self), (0,0))
                self.num_agents += 1
                self.agent_id += 1
                self.added_agents+=1
            
            elif self.num_steps % 10 == 0 and self.grid.is_cell_empty(0,0):
                self.grid.place_agent(Car(f"car_{self.agent_id}", self), (0,0))
                self.num_agents += 1
                self.agent_id += 1
                self.added_agents+=1
            
            elif self.num_steps % 10 == 0 and self.grid.is_cell_empty(0,0):
                self.grid.place_agent(Car(f"car_{self.agent_id}", self), (0,0))
                self.num_agents += 1
                self.agent_id += 1
                self.added_agents+=1
            
            elif self.num_steps % 10 == 0 and self.grid.is_cell_empty(0,0):
                self.grid.place_agent(Car(f"car_{self.agent_id}", self), (0,0))
                self.num_agents += 1
                self.agent_id += 1
                self.added_agents+=1

        if self.num_steps % 10 == 0 and self.added_agents == 0: 
            self.running = False
        
        self.added_agents = 0