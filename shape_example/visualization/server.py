import mesa

from .model import MSModel, Walls, Walker


def agent_draw(agent):
    portrayal = None
    if agent is None:
        # Actually this if part is unnecessary, but still keeping it for
        # aesthetics
        pass
    elif isinstance(agent, Walker):
        portrayal = {"Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "blue",
            "r": 0.5}
    elif isinstance(agent, Walls):
        portrayal = {"Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "black",
            "w": 1,
            "h": 1}
    return portrayal


width = 250
height = 120
num_agents = 100
pixel_ratio = 5
grid = mesa.visualization.CanvasGrid(
    agent_draw, width, height, width * pixel_ratio, height * pixel_ratio
)
server = mesa.visualization.ModularServer(
    MSModel,
    [grid],
    "MS Model",
    {"N": num_agents, "width": width, "height": height},
)
server.max_steps = 10
