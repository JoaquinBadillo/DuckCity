from TrafficSimulation.agents import *
from TrafficSimulation.model import TrafficModel
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
import os

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

width = 0
height = 0

with open(f'{os.path.dirname(__file__)}/TrafficSimulation/city_files/2021_base2.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

print(width, height)
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

server = ModularServer(TrafficModel, [grid], "Traffic")
                       
server.port = 8521 # The default
server.launch()