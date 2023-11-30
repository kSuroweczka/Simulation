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
        self.is_occupied = is_obstacle
        self.static_floor_field: 10000

class StudentAgent(mesa.Agent):
    def __init__(self, unique_id, model, position: (int, int), initial_state=State.ACTIVE):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.current_position = position
        self.parent = None
        # self.target_exit: Exit = None
        # self.floor_field = self.calculate_static_floor_field(self.target_exit)

    def move(self):
        
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        possible_steps = [cell for cell in possible_steps if cell not in self.model.walls]

        # here use algotithm to find the shortest path to exit
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        is_not_occupied = self.model.grid.get_cell_list_contents([new_position]) == 0
        if is_not_occupied:
            self.model.grid.move_agent(self, new_position)
            self.position = new_position

    def calculate_static_floor_field(self):
        paths = []
        lengths = []
        open_list = []
        closed_list = []
        G=[]
        H=[]
        F=[]
        current_cell = Cell(self.current_position, False)
        open_list.append(self.current_position)


        for exit in self.model.exits:
            G.append(self.G(exit.position[0], exit.position[1]))
            H.append(self.Heuristic(exit.position[0], exit.position[1], exit))
            F.append(self.F(exit.position[0], exit.position[1], exit))
            open_list.append(exit.position)

        while len(open_list) > 0:
            fMin = min(F) 
            fMin_index = F.index(fMin)
            proposed_exit = open_list[fMin_index]
            closed_list.append(proposed_exit)

            for neighbor in self.model.grid.get_neighborhood(self.current_position, moore=True, include_center=True):
                if neighbor not in closed_list and neighbor.state != State.OBSTACLE:
                    if neighbor not in open_list:
                        G.append(self.G(neighbor.position[0], neighbor.position[1]))
                        H.append(self.Heuristic(neighbor.position[0], neighbor.position[1], self.model.exits[fMin_index]))
                        F.append(self.F(neighbor.position[0], neighbor.position[1], self.model.exits[fMin_index]))
                        neighbor.parent = current_cell
                        open_list.append(neighbor)
                    else:
                        if self.G(neighbor.position[0], neighbor.position[1]) < G[open_list.index(neighbor.position[0], neighbor.position[1])]:  ####?????
                            G[open_list.index(neighbor.position[0], neighbor.position[1])] = self.G(neighbor.position[0], neighbor.position[1])
                            neighbor.parent = current_cell
                if proposed_exit in open_list:
                    paths.append(open_list)
                    lengths.append(F[open_list.index(neighbor.position[0], neighbor.position[1])])
        MinLength = min(lengths)
        MinLength_index = lengths.index(MinLength)
        return paths[MinLength_index], lengths[MinLength_index]

    def Heuristic(self, x, y, exit: Exit):
        return 10 *(abs(x - exit.position[0]) + abs(y - exit.position[1]))
    
    def G(self, x, y):
        return 10 + self.floor_field[x][y]
    
    def F(self, x, y, exit: Exit):
        return self.G(x, y) + self.Heuristic(x, y, exit)
    
    def step(self):
        self.move()


# def a_star_algorithm(self, obstacles, exit):
#         current_position = self.current_position
#         exit_position = exit.position

#         open_list = []
#         closed_list = []
#         path = []
#         path_length = 0

#         open_list.append((current_position, path_length))

#         while len(open_list) > 0:
#             current_position, path_length = open_list.pop(0)
#             closed_list.append(current_position)

#             if current_position == exit_position:
#                 path.append(current_position)
#                 break

#             neighbors = self.model.grid.get_neighborhood(current_position, moore=True, include_center=True)
#             neighbors = [cell for cell in neighbors if cell not in obstacles]

#             for neighbor in neighbors:
#                 if neighbor not in closed_list:
#                     open_list.append((neighbor, path_length + 1))
#                     closed_list.append(neighbor)

#         return path, path_length