import mesa
from utils import State

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder



class Exit(mesa.Agent):    
    def __init__(self, unique_id, model, position, state=State.EXIT):
        super().__init__(unique_id, model)
        self.state = state
        self.escaped_students = 0
        self.position = position

class Walls(mesa.Agent):
    def __init__(self, unique_id, model, position, state=State.OBSTACLE):
        super().__init__(unique_id, model)
        self.state = state
        self.position = position
    
class Cell:
    def __init__(self, position: (int, int), is_obstacle: bool):
        self.position = position
        self.g =0
        self.h =0
        self.f =0
        self.parent = None
        self.is_obstacle = is_obstacle


LIST_OF_CELLS: list[Cell()]    ### nie wiem czy ona ma byc tutaj

class StudentAgent(mesa.Agent):
    def __init__(self, unique_id, model, position: (int, int), initial_state=State.ACTIVE, exits_list=list[Exit]):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.current_position = position
        self.parent = None
        self.exits = exits_list
        # self.target_exit: Exit = None
        # self.floor_field = self.calculate_static_floor_field(self.target_exit)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        possible_steps = [cell for cell in possible_steps if cell not in self.model.walls]

        # here use algotithm to find the shortest path to exit
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        for exit in self.exits:
            self.aStarSearch(self.current_position, exit)

        is_not_occupied = self.model.grid.get_cell_list_contents([new_position]) == 0
        if is_not_occupied:
            self.model.grid.move_agent(self, new_position)
            self.position = new_position

    # wieksza czesc znajduje sie w pliku copy-agents.py
    def aStarSearch(self, current_position, exit: Exit):  ### czyli musi byc wywoływana w kazdym ruchu i dla kazdego exita
        obstacles = self.Walls.position
        open_list: list[(int,int)]
        closed_list: list[(int,int)]
        g=[]
        h=[]
        f=[]

        # TODO: - zeby komorki mialy swoje stany
        if self.model.grid.is_cell_empty(current_position):  # step 1 ### tutaj czy ten wrunek wystarczy
            g[0] = 0 ### dla punktu startowego
            h[0] = self.H(current_position, exit)
            f[0] = g[0] + h[0]

            open_list.append(current_position)

            # while len(open_list) > 0:
            #     for neighbor in self.model.grid.get_neighborhood(self.current_position, moore=True, include_center=True):
        pass
                    
    def H(self, position,  exit: Exit):
        return 10 *(abs(position[0] - exit.position[0]) + abs(position[1] - exit.position[1]))
    
    def G(self, G_parent_value):    ### tutaj kiedys zmienic na 10 lub 14
        return 10 + G_parent_value
    
    def step(self):
        self.move()
