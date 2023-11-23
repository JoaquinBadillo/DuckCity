from agents import *
from model import TrafficModel
from mesa.visualization import CanvasGrid, BarChartModule
from mesa.visualization import ModularServer
import os

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {
                 "Shape": "rect",
                 "Filled": "true",
                 "Color": "red",
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
        portrayal["Color"] = "red" if not agent.state else "green"
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

with open(f'{os.getcwd()}/city_files/2021_base2.txt') as baseFile:
    lines = baseFile.readlines()
    width = len(lines[0])-1
    height = len(lines)

model_params = {
    "num_agents": 5,
    "width": 50,
    "height": 50
}

print(width, height)
grid = CanvasGrid(agent_portrayal, width, height, 500, 500)

server = ModularServer(TrafficModel, [grid], "Traffic", model_params)
                       
server.port = 8521 # The default
server.launch()