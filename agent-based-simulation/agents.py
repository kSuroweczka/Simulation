import mesa
import heapq
import random
from utils import State
import numpy as np  

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

class Bench(mesa.Agent):
    def __init__(self, unique_id, model, position, state=State.OBSTACLE):
        super().__init__(unique_id, model)
        self.state = state
        self.position = position

class Tree(mesa.Agent):
    def __init__(self, unique_id, model, position, state=State.OBSTACLE):
        super().__init__(unique_id, model)
        self.state = state
        self.position = position
        self.size = random.randint(4,5)

class StudentAgent(mesa.Agent):
    def __init__(self, unique_id, model, position: (int, int), initial_state=State.ACTIVE, obstacles=[], exits=[]):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.current_position = position
        self.parent = None
        self.obstacles = obstacles
        self.exits = exits
        self.target_exit: (int,int)
        self.path_to_exit: list[(int,int)] = None

        CELLS_OCCUPIED_BY_STUDENTS.append(position)
    
    def calculate_nearest_exit(self, position, exit):
        return np.linalg.norm(np.array(position) - np.array(exit))
        
    def find_target_exit(self):
        self.target_exit = min(self.exits, key=lambda exit: self.calculate_nearest_exit(self.current_position, exit))
        self.path_to_exit, _ = self.aStarSearch(self.current_position, self.target_exit)
        
        

    # def find_target_exit(self): 
    #     path =[]
    #     cost =[]
        
    #     for exit in self.exits:
    #         path_i,cost_i = self.aStarSearch(self.current_position,exit)
    #         path.append(path_i)
    #         cost.append(cost_i)
    
    #     min_cost = min(cost)
    #     min_cost_index = cost.index(min_cost)

    #     self.path_to_exit = path[min_cost_index] 
    #     self.target_exit = self.path_to_exit[-1]
    

    def aStarSearch(self, start, stop):
        open_lst = [(0, start)]  
        heapq.heapify(open_lst)  

        closed_lst = set()

        g = {start: 0}

        par = {start: start}

        while open_lst:
            _, n = heapq.heappop(open_lst)

            if n == stop:
                return self.reconstruct_path(par, n), g[n]

            x, y = n
            neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y),
                         (x + 1, y), (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]

            for m in neighbors:
                if m not in closed_lst and m not in self.obstacles:
                    tentative_g_score = g[n] + 10

                    if m not in g or tentative_g_score < g[m]:
                        g[m] = tentative_g_score
                        f_score = tentative_g_score + self.H(m, stop)
                        heapq.heappush(open_lst, (f_score, m))
                        par[m] = n

            closed_lst.add(n)

        print('Path does not exist!')
        return None

    def reconstruct_path(self, par, current):
        path = []
        while par[current] != current:
            path.append(current)
            current = par[current]
        path.append(current)
        return path[::-1]
    
    def move(self):
        if len(self.path_to_exit) == 0:
            print("Goal reached")
            self.state = State.ESCAPED

        else:
            nearest_exit = min(self.exits, key=lambda exit: self.calculate_nearest_exit(self.current_position, exit))
            if nearest_exit != self.target_exit:
                self.target_exit = nearest_exit
                self.path_to_exit, _ = self.aStarSearch(self.current_position, self.target_exit)
           
            new_position = self.path_to_exit[0]
            if new_position not in self.obstacles:
                self.model.grid.move_agent(self, new_position)
                CELLS_OCCUPIED_BY_STUDENTS.remove(self.current_position)
                if self.current_position != self.path_to_exit[-1]:
                    self.path_to_exit.pop(0)
                    CELLS_OCCUPIED_BY_STUDENTS.append(new_position)
                self.current_position = new_position

                    
                
                    
    def H(self, position, exit):
        position = np.array(position)
        exit = np.array(exit)
        return 10 * np.sum(np.abs(position - exit))
    
    def step(self):
        self.move()
        
    # def random_move(self):
    #     possible_moves = self.model.grid.get_neighborhood(self.current_position, moore=True, include_center=False)
    #     new_position = random.choice(possible_moves)
    #     while new_position in self.obstacles:
    #         new_position = random.choice(possible_moves)
    #     self.model.grid.move_agent(self, new_position)
    #     CELLS_OCCUPIED_BY_STUDENTS.remove(self.current_position)
    #     CELLS_OCCUPIED_BY_STUDENTS.append(new_position)
    #     self.current_position = new_position
    #     self.path_to_exit, _ = self.aStarSearch(self.current_position, self.target_exit)
    #     self.target_exit = self.path_to_exit[-1]
        
    
        
