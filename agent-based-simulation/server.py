from agents import StudentAgent, Walls, Exit, Bench, Tree
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
    elif isinstance(agent, Bench):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": Colors['BENCH'],
                     "w": 1,
                     "h": 1
                     }
    elif isinstance(agent, Tree):
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": Colors['TREE'],
                     "r": agent.size,
                     }
    elif isinstance(agent, Exit):
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": Colors['EXIT'],
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
        "Students", 200, 100, 500, description="Number of Students"),
    "move_probability": mesa.visualization.Slider(
        "Move Probability", 0.8, 0.0, 1.0, 0.1, description="Move Probability"),
    "random_move_probability": mesa.visualization.Slider(
        "Random Move Probability", 0.15, 0.0, 1.0, 0.1, description="Random Move Probability"),
}

grid = mesa.visualization.CanvasGrid(person_portrayal, WIDTH, HEIGHT, WIDTH * PIXEL_RATIO, HEIGHT * PIXEL_RATIO)

server = mesa.visualization.ModularServer(EvacuationModel, [grid], "Evacuation Model", model_params)
