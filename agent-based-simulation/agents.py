import mesa
import heapq
import random

from utils import *
import numpy as np

class Exit(mesa.Agent):
    def __init__(self, unique_id, model, position, state=State.EXIT):
        super().__init__(unique_id, model)
        self.state = state
        self.position = position
        self.escaped_students = 0

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
    def __init__(self, unique_id, model, position, move_probability, random_move_probability, initial_state=State.ACTIVE, obstacles=[], exits=[]):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.current_position = tuple(position) 
        self.obstacles = obstacles
        self.exits = exits
        self.new_path_needed = False
        self.target_exit = None
        self.path_to_exit = []
        self.step_counter = 0
        self.move_probability = move_probability
        self.random_move_probability = random_move_probability
        self.exits_pos =    [          (96,23),
            (116,2),
             (144,2),
         (146,108),
              (116,117)
        ]
        # self.exit_dict = {
        #  (96,22):(96,23),
        #     (117,18):(116,2),
        #      (145,18):(144,2),
        #  (145,97):(146,108),
        #       (115,106):(116,117)
        # }
        CELLS_OCCUPIED_BY_STUDENTS.append(self.current_position)


    def calculate_nearest_exit(self, position, exit):
        return abs(position[0] - exit[0]) + abs(position[1] - exit[1])
    

    def find_target_exit(self):
        self.target_exit = min(self.exits, key=lambda exit: self.calculate_nearest_exit(self.current_position, exit))
        self.path_to_exit, _ = self.aStarSearch(self.current_position, self.target_exit)

        if self.target_exit in EXITS:
            EXITS[self.target_exit] += 1
        else:
            EXITS[self.target_exit] = 1
    
    def evaluate_nearest_exit(self):
        distances = []
        for exit in self.exits_pos:
            distance = self.calculate_nearest_exit(self.current_position, exit)
            distances.append((distance, exit))
        distances.sort() 
        
        two_nearest_exits = distances[:2]  

        nearest_exit = None
        min_score = float('inf')
        for distance, exit in two_nearest_exits:
            traffic = self.model.traffic_at_exits[exit]
            
            score = 2*distance + traffic
            if score < min_score:
                min_score = score
                nearest_exit = exit
        
            else:
                continue

        return nearest_exit



    def aStarSearch(self, start, stop):
        if start == stop:
            return [start], 0

        open_lst = [(0, start)]
        heapq.heapify(open_lst)
        closed_lst = set()
        g = {start: 0}
        par = {start: start}

        while open_lst:
            _, n = heapq.heappop(open_lst)

            if n == stop:
                return self.reconstruct_path(par, n), g[n]

            neighbors = self.model.grid.get_neighborhood(n, moore=True, include_center=False)
            for m in neighbors:
                if m not in closed_lst and m not in self.obstacles:
                    tentative_g_score = g[n] + self.H(n, m)
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
        while current != par[current]:
            path.append(current)
            current = par[current]
        path.append(current)
        return path[::-1]

    def move(self):
        if self.state == State.ESCAPED or not self.path_to_exit:
            return
        new_position = self.path_to_exit.pop(0)
        if new_position not in self.obstacles:
            self.model.grid.move_agent(self, new_position)
            CELLS_OCCUPIED_BY_STUDENTS.remove(self.current_position)
            CELLS_OCCUPIED_BY_STUDENTS.append(new_position)
            self.current_position = new_position
            self.model.grid_matrix[self.current_position] -= 1 
            self.current_position = new_position
            self.model.grid_matrix[self.current_position] += 1
            
            if self.current_position == self.target_exit:
                self.state = State.ESCAPED
                self.model.num_students -= 1
            
            

            DENSITY_MATRIX[new_position[0]][new_position[1]] += 1


    def H(self, position, exit):
        return 10 * sum(abs(a - b) for a, b in zip(position, exit))

    def add_random_move(self):
        if len(self.path_to_exit) > 8:
            next_move = self.path_to_exit[0]
            d = (next_move[0] - self.current_position[0], next_move[1] - self.current_position[1])

            direction_to_moves = {
                (0, 1): [(-1, 1), (1, 1)],
                (0, -1): [(-1, -1), (1, -1)],
                (1, 0): [(1, -1), (1, 1)],
                (-1, 0): [(-1, -1), (-1, 1)],
                (1, 1): [(1, 0), (0, 1)],
                (-1, -1): [(-1, 0), (0, -1)],
                (1, -1): [(1, 0), (0, -1)],
                (-1, 1): [(-1, 0), (0, 1)]
            }

            moves = direction_to_moves.get(d, [(0, 0)])  
            move = random.choice(moves)
            new_position = (self.current_position[0] + move[0], self.current_position[1] + move[1])

            if new_position not in self.obstacles:
                self.path_to_exit[0] = new_position



    def step(self):

        if self.new_path_needed:
            self.find_target_exit()
            self.new_path_needed = False
       
        random_move = random.random() < self.random_move_probability
        
    
        if random_move:
            self.add_random_move()

        do_move = random.random() < self.move_probability
        if do_move: 
            self.move()

        if self.state != State.ESCAPED and not self.path_to_exit:
            self.find_target_exit()
        

