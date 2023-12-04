import mesa
from utils import State
import heapq

global CELLS_OCCUPIED_BY_STUDENTS
CELLS_OCCUPIED_BY_STUDENTS =[]

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


class StudentAgent(mesa.Agent):
    def __init__(self, unique_id, model, position: (int, int), initial_state=State.ACTIVE, exits_list=list[Exit], walls_list=list[(int,int)]):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.current_position = position
        self.parent = None
        self.walls = walls_list
        self.exits = exits_list
        self.target_exit: (int,int)
        self.path_to_exit: list[(int,int)] = None
        CELLS_OCCUPIED_BY_STUDENTS.append(position) 

    def find_target_exit(self): 
        path =[]
        cost =[]
        
        for exit in self.exits:
            path_i,cost_i = self.aStarSearch(self.current_position,exit)
            path.append(path_i)
            cost.append(cost_i)
    
        min_cost = min(cost)
        min_cost_index = cost.index(min_cost)

        self.path_to_exit = path[min_cost_index] 
        self.target_exit = self.path_to_exit[-1]
    
    def aStarSearch(self, start, stop) -> (list[(int,int)],int): 
        open_lst = set([start]) 
        closed_lst = set([])

        g = {}
        g[start] = 0

        par = {}   ### parent
        par[start] = start
 
        while len(open_lst) > 0:
            n = None

            for v in open_lst:
                if n == None or g[v] + self.H(v,stop) < g[n] + self.H(n, stop):
                    n = v
 
            if n == None:
                print('Path does not exist!')
                return None

            if n == stop:
                reconst_path = []
                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]
                reconst_path.append(start)
                reconst_path.reverse()
                return reconst_path, len(reconst_path)
            
            x=n[0]
            y=n[1]
            neighbors = [ (x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y),(x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]
            for m in neighbors:
                if m not in open_lst and m not in closed_lst and m not in self.walls:
                    open_lst.add(m)
                    par[m] = n
                    g[m] = g[n] + 10

                else:
                    if m not in self.walls and g[m] > g[n] + 10:
                        g[m] = g[n] + 10
                        par[m] = n
 
                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)
            open_lst.remove(n)
            closed_lst.add(n)
 
        print('Path does not exist!')
        return None

    def move(self):
        # possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        # possible_steps = [cell for cell in possible_steps if cell not in self.model.walls]

        # Stary kod
        # here use algotithm to find the shortest path to exit
        # new_position = self.random.choice(possible_steps)
        # print("NEW: ", new_position)
        # self.model.grid.move_agent(self, new_position)

        # is_not_occupied = self.model.grid.get_cell_list_contents([new_position]) == 0
        # print("is: ",self.model.grid.get_cell_list_contents([new_position])  )
        # if is_not_occupied:
        #     self.model.grid.move_agent(self, new_position)
        #     self.position = new_position

        if len(self.path_to_exit) == 0:
            print("CEL OSIAGNIETY")
            # self.model.grid.remove_agent(self)
            self.state = State.ESCAPED
            self.currrent_position = self.current_position
        else:
            new_position = self.path_to_exit[0] 

            # is_not_occupied = self.model.grid.get_cell_list_contents([new_position]) == 0
            if new_position not in self.walls :
                self.model.grid.move_agent(self, new_position)
                CELLS_OCCUPIED_BY_STUDENTS.remove(self.current_position)
                if self.current_position != self.path_to_exit[-1]: 
                    self.path_to_exit.remove(self.path_to_exit[0])
                    CELLS_OCCUPIED_BY_STUDENTS.append(new_position)
                self.current_position = new_position  
            else:
                self.currrent_position = self.current_position


   

                    
    def H(self, position,  exit):
        return 10 *(abs(position[0] - exit[0]) + abs(position[1] - exit[1]))
    
    def step(self):
        self.move()
