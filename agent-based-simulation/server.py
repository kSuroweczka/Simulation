from agents import StudentAgent, Walls
from utils import *
import mesa
from evacuation_model import EvacuationModel

def person_portrayal(agent):
    portrayal = {}

    if agent is None:
        return
    elif isinstance(agent, Walls):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": Colors['WALL'],
                     "w": 1,
                     "h": 1
                     }
    elif isinstance(agent, StudentAgent):
        portrayal = {"Shape": "circle",
                     "r": 0.8,
                     "Layer": 1,
                     "Filled": "true",
                     "Color": Colors['STUDENT']                     
                     }

    return portrayal

model_params = {
    "num_students": mesa.visualization.Slider(
        "Students", 100, 1, 300, description="Number of Students"),   
}



grid = mesa.visualization.CanvasGrid(person_portrayal, WIDTH, HEIGHT, WIDTH * PIXEL_RATIO, HEIGHT * PIXEL_RATIO)

server = mesa.visualization.ModularServer(EvacuationModel, [grid], "Evacuation Model", model_params)
