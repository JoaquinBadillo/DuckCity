# Traffic Simulation Model
# Defines a Multigrid model for the traffic simulation.

# The grid will be initialized with roads and stoplights using a document. Also,
# a given number of cars will be initialized, but after each iteration more cars
# will be added to the grid.

# Last Update: 20/Nov/2023
# Joaquín Badillo, Pablo Bolio

from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid

from agents import (
    Car,
    Destination,
    Obstacle,
    Road,
    Stoplight
)

from utilities import (
    Colors,
    Directions
)

from pathfinder import GPS

import json
import os

class TrafficModel(Model):
    def __init__(self,
                 num_agents=10,
                 width=50,
                 height=50):
        super().__init__()

        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        # Non-Omniscient GPS
        # Stored in the model to avoid dumb replication
        self.gps = GPS(self)
        
        # Stats
        self.num_steps = 0
        self.num_agents = num_agents
        self.agent_id = 1
        self.added_agents = 0
        self.num_arrivals = 0
        self.traffic_lights = []
        self.destinations = []

        # Load map from file
        dataDictionary = json.load(
            open(f"{os.getcwd()}/city_files/mapDictionary.json")
        )

        with open(f'{os.getcwd()}/city_files/2021_base2.txt') as city:
            lines = city.readlines()
            self.width = len(lines[0])-1
            self.height = len(lines)
            
            self.grid = MultiGrid(self.width, self.height, torus = False) 
            self.schedule = RandomActivation(self)

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
                        self.destinations.append((c, self.height - r - 1))

        self.running = True

    def step(self):
        self.schedule.step()
        self.num_steps += 1
        
        if self.num_steps % 10 != 0:
            return
        
        corners = [
            (0,0),
            (self.width -1,0),
            (0,self.height -1), 
            (self.width -1,self.height -1)
        ]

        for corner in corners:
            car = next(
                filter(lambda agent: type(agent) == Car, self.grid.get_cell_list_contents([corner])),
                None
            )

            if car is None:
                agent = Car(
                    f"car_{self.agent_id}", 
                    self,
                    self.random.choice(self.destinations)
                )

                self.grid.place_agent(agent, corner)
                agent.route = self.gps.astar(agent.pos, agent.destination)
                self.schedule.add(agent)

                self.num_agents += 1
                self.agent_id += 1
                self.added_agents+=1

        if self.added_agents == 0: 
            self.running = False
        
        self.added_agents = 0