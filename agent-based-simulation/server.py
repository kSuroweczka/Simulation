from agents import StudentAgent, JaguarAgent
from utils import State
import mesa
from evacuation_model import EvacuationModel

#green
LEGAL_STUDENT = "#2ca02c"

#orange
ILLEGAL_STUDENT = "#ff7f0e"

#blue
JAGUAR = "#1f77b4"

#red
BANNED_STUDENT = "#d62728"


def person_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {}

    # update portrayal characteristics for each Person object
    if isinstance(agent, StudentAgent):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 0
        portrayal["Filled"] = "true"

        color = LEGAL_STUDENT

        # set agent color based on status
        if agent.state == State.ILLEGAL:
            color = ILLEGAL_STUDENT
        if agent.state == State.BANNED:
            color = BANNED_STUDENT

        portrayal["Color"] = color


    if isinstance(agent, JaguarAgent):
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.5
        portrayal["Layer"] = 1
        portrayal["Filled"] = "true"

        portrayal["Color"] = JAGUAR

    return portrayal

model_params = {

    "num_jaguars": mesa.visualization.Slider(
        "Security Guards", 1, 1, 10, description="Number of Security Guards"),
    "num_students": mesa.visualization.Slider(
        "Students", 25, 1, 200, description="Number of Students"),
    "proc_illegal_students": mesa.visualization.Slider(
        "Illegal Students", 0, 1, 100, description="Percentage of Illegal Students"),    
    "width": 20,
    "height": 20,
}

chart_element = mesa.visualization.ChartModule(
    [
        {"Label": "BANNED", "Color": BANNED_STUDENT},
    ],
    data_collector_name='datacollector'
)

canvas_element = mesa.visualization.CanvasGrid(person_portrayal, 20, 20, 500, 500)

server = mesa.visualization.ModularServer(EvacuationModel, [canvas_element], "Evacuation Model", model_params)
