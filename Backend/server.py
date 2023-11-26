from TrafficSimulation.agents import *
from TrafficSimulation.model import TrafficModel
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
import os

import argparse

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {
                 "Shape": "rect",
                 "Filled": "true",
                 "Color": "black",
                 "Layer": 2,
                 "w": 1,
                 "h": 1
                }

    if (isinstance(agent, Road)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 0
    
    if (isinstance(agent, Destination)):
        portrayal["Color"] = "lightgreen"
        portrayal["Layer"] = 0

    if (isinstance(agent, Stoplight)):
        portrayal["Color"] = agent.state.name.lower()
        portrayal["Layer"] = 1
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    if (isinstance(agent, Obstacle)):
        portrayal["Color"] = "cadetblue"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.8
        portrayal["h"] = 0.8

    return portrayal

if __name__ == "__main__":
    width = 0
    height = 0

    parser = argparse.ArgumentParser(description='Run the traffic simulation.')
    parser.add_argument('--cycles', type=int, default=10, help='Number of cycles to run the simulation for.')
    args = parser.parse_args()

    with open(f'{os.path.dirname(__file__)}/TrafficSimulation/city_files/2021_base2.txt') as baseFile:
        lines = baseFile.readlines()
        width = len(lines[0])-1
        height = len(lines)

    print(width, height)
    grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

    server = ModularServer(TrafficModel, [grid], "Traffic", {"agent_cycle": args.cycles})
                        
    server.port = 8521 # The default
    server.launch()