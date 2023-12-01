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

from .agents import (
    Car,
    Destination,
    Obstacle,
    Road,
    Stoplight
)

from .utilities import (
    Colors,
    Directions
)

from .pathfinder import GPS
import os

import requests
from threading import Thread

class TrafficModel(Model):
    def __init__(self,
                 width=50,
                 height=50,
                 agent_cycle=10,
                 post_cycle=100,
                 self_url=None,
                 limit=1000):
        super().__init__()

        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        
        # Non-Omniscient GPS
        # Stored in the model to avoid dumb replication
        self.gps = GPS(self)
        
        # Stats
        self.num_steps = 0
        self.num_agents = 0
        self.agent_id = 1
        self.added_agents = 0
        self.num_arrivals = 0
        self.limit = limit
        self.traffic_lights = []
        self.destinations = []

        self.agent_cycle = agent_cycle

        self.url = self_url
        self.post_cycle = post_cycle

        self.arrived_agents = []

        with open(f'{os.path.dirname(__file__)}/city_files/2023_base.txt') as city:
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

                    elif col in ["y", "Y", "h", "H"]:
                        stoplight = Stoplight(f"tl_{r*self.width+c}", self, Colors.GREEN, 5)
                        self.grid.place_agent(stoplight, (c, self.height - r - 1))
                        self.traffic_lights.append(stoplight)

                        if col == "y":
                            road = Road(f"r_{r*self.width+c}", self, (Directions.DOWN,))
                            self.grid.place_agent(road, (c, self.height - r - 1))
                            stoplight.state = Colors.RED
                        elif col == "Y":
                            road = Road(f"r_{r*self.width+c}", self, (Directions.UP,))
                            self.grid.place_agent(road, (c, self.height - r - 1))
                            stoplight.state = Colors.RED
                        elif col == "h":
                            road = Road(f"r_{r*self.width+c}", self, (Directions.LEFT,))
                            self.grid.place_agent(road, (c, self.height - r - 1))
                        elif col == "H":
                            road = Road(f"r_{r*self.width+c}", self, (Directions.RIGHT,))
                            self.grid.place_agent(road, (c, self.height - r - 1))
                        
                    elif col == "#":
                        agent = Obstacle(f"ob_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))

                    elif col == "D":
                        agent = Destination(f"d_{r*self.width+c}", self)
                        self.grid.place_agent(agent, (c, self.height - r - 1))
                        self.destinations.append((c, self.height - r - 1))

        
        self.corners = [(0,0), (self.width -1,0), (0,self.height -1), (self.width -1,self.height -1)]
        self.running = True

        valid_corners = filter(
            lambda cell: not any(x for x in self.grid.get_cell_list_contents([cell]) 
                                 if isinstance(x, Car)),
            self.corners
        )

        for corner in valid_corners:
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
    
    def post(self, num_arrivals):
        if self.url is None:
            return

        print(f"Sending POST request to {self.url}")
        data = {
            "year": 2023,
            "classroom": 301,
            "name": "Ducking (Joaco y Bolio)",
            "num_cars": num_arrivals
        }

        try:
            requests.post(self.url, json = data)
        except:
            print("Error sending POST request")

    def step(self):
        while (len(self.arrived_agents) > 0):
            agent = self.arrived_agents.pop()
            self.num_arrivals += 1
            self.schedule.remove(agent)
            self.grid.remove_agent(agent)
            self.num_agents -= 1
        
        for stoplight in self.traffic_lights:
            stoplight.step()
            
        self.schedule.step()
        self.num_steps += 1

        if self.num_steps % self.post_cycle == 0: 
            Thread(target=self.post, args=(self.num_arrivals,)).start()
        
        if self.num_steps == self.limit: 
            self.running = False
            return
        
        if self.num_steps % self.agent_cycle != 0: return
        
        valid_corners = filter(
            lambda cell: not any(x for x in self.grid.get_cell_list_contents([cell]) 
                                 if isinstance(x, Car)),
            self.corners
        )

        for corner in valid_corners:
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