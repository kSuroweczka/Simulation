import mesa
from agents import StudentAgent, Walls, Exit, Bench, Tree
from utils import *
import pandas as pd
import os
 

class EvacuationModel(mesa.Model):

    def __init__(self, num_students, move_probability, random_move_probability, width=WIDTH, height=HEIGHT, num_steps=80):
        self.width = width
        self.height = height
        self.grid_matrix = np.zeros((width, height))  
        self.num_students = num_students
        self.num_steps = num_steps
        self.all_exits = [(96,23), (116,2), (144,2), (146,108), (116,117)]           
        self.exits_to_evaluate = list(self.all_exits)  
        self.buffer_update_interval = 5
        self.current_step = 0
        self.agents_to_evaluate = []
        self.move_probability = move_probability
        self.random_move_probability = random_move_probability
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.traffic_at_exits = {exit_pos: 0 for exit_pos in self.all_exits}  
        self.wall_pos, self.exits, self.inside_exits, self.bench_pos, self.tree_pos = self.create_map()
        self.obstacles = self.wall_pos + self.bench_pos + self.tree_pos
        self.create_students_version_3()
        self.running = True
        self.active_students = self.num_students

    def create_students(self):
        for i in range(self.num_students):
            x = self.random.randrange(10, 230)
            y = self.random.randrange(30, 100)
            while (x, y) in self.obstacles or (x, y) in self.exits:
                x = self.random.randrange(10, 230)
                y = self.random.randrange(30, 100)
            
            pos = (x, y)
            student = StudentAgent(i, self, pos, self.move_probability, self.random_move_probability, State.ACTIVE, obstacles=self.obstacles, exits=self.inside_exits) #### potem zmienic exits i walls na cos z model
            DENSITY_MATRIX[x][y] += 1

            self.grid.place_agent(student, pos)
            self.schedule.add(student)

            student.find_target_exit()   

        df = pd.DataFrame([EXITS])
        df.to_csv("../agent-based-simulation/analysis/exits/exits.csv")
    
    def create_students_version_2(self):
        for i in range(self.num_students):
            x = self.random.randrange(150, 220)
            y = self.random.randrange(40, 90)
            while (x, y) in self.obstacles or (x, y) in self.exits:
                x = self.random.randrange(150, 220)
                y = self.random.randrange(40, 90)
            
            pos = (x, y)
            student = StudentAgent(i, self, pos, self.move_probability, self.random_move_probability, State.ACTIVE, obstacles=self.obstacles, exits=self.inside_exits) #### potem zmienic exits i walls na cos z model
            DENSITY_MATRIX[x][y] += 1

            self.grid.place_agent(student, pos)
            self.schedule.add(student)

            student.find_target_exit()   

        df = pd.DataFrame([EXITS])
        df.to_csv("../agent-based-simulation/analysis/exits/exits.csv")

    def create_students_version_3(self):
        for i in range(self.num_students):
            x = self.random.randrange(110, 150)
            y = self.random.randrange(50, 80)
            while (x, y) in self.obstacles or (x, y) in self.exits:
                x = self.random.randrange(110, 150)
                y = self.random.randrange(50, 80)
            
            pos = (x, y)
            student = StudentAgent(i, self, pos, self.move_probability, self.random_move_probability, State.ACTIVE, obstacles=self.obstacles, exits=self.inside_exits) #### potem zmienic exits i walls na cos z model
            DENSITY_MATRIX[x][y] += 1

            self.grid.place_agent(student, pos)
            self.schedule.add(student)

            student.find_target_exit()   

        df = pd.DataFrame([EXITS])
        df.to_csv("../agent-based-simulation/analysis/exits/exits.csv")

    def create_map(self):
        with open('./map_template.csv', 'r'):
            df = pd.read_csv('./map_template.csv', sep=',', header=0, index_col=0)
            data = df.values
            data = data.transpose()
        
        wall_pos = []
        trees_pos = []
        benches_pos = []
        exits = {}
        inside_exits = {(96,19),(96,20),(96,21),(96,22),(96,23), (96,24),(96,25),
                        (114,2),(115,2),(116,2),(117,2),
                        (144,2),(145,2),(146,2),(147,2),
                        (114,117), (115,117),(116,117),(117,117),
                        (144,108),(145,108),(146,108),(147,108)}

        for x in range(WIDTH):
            for y in range(HEIGHT):
                if data[y][x] == 1:
                    pos = (x, y)
                    wall = Walls(f'{x}-{y}', self, pos, State.OBSTACLE)
                    wall_pos.append(pos)
                    self.grid.place_agent(wall, pos)
                elif data[y][x] == 2:
                    pos = (x, y)
                    exit = Exit(f'{x}-exit-{y}', self, pos, State.EXIT)
                    self.grid.place_agent(exit, pos)
                    exits[pos] = exit
                elif data[y][x] == 3:
                    pos = (x, y)
                    bench = Bench(f'{x}-bench-{y}', self, pos, State.OBSTACLE)
                    self.grid.place_agent(bench, pos)
                    benches_pos.append(pos)
                elif data[y][x] == 4:
                    pos = (x, y)
                    tree = Tree(f'{x}-tree-{y}', self, pos, State.OBSTACLE)
                    self.grid.place_agent(tree, pos)
                    trees_pos.append(pos)
                
        return wall_pos, exits, inside_exits, benches_pos, trees_pos 
        
    
    def calculate_traffic_for_all_exits(self):
        traffic_at_exits = {}
      
        buffer_size = 20
        for exit_pos in self.exits_to_evaluate:
            x_min = max(0, exit_pos[0] - buffer_size)
            x_max = min(self.width, exit_pos[0] + buffer_size + 1)
            y_min = max(0, exit_pos[1] - buffer_size)
            y_max = min(self.height, exit_pos[1] + buffer_size + 1)

        
            area_count = np.sum(self.grid_matrix[x_min:x_max, y_min:y_max])
            self.traffic_at_exits[exit_pos] = area_count
 
            
        return traffic_at_exits
    def evaluate_student_path(self):
        num_agents_to_evaluate = max(1, int(self.active_students * 0.1))  
        for _ in range(num_agents_to_evaluate):
            if self.agents_to_evaluate:
                agent = self.agents_to_evaluate.pop(0)  
                new_target_exit = agent.evaluate_nearest_exit()
                if new_target_exit != agent.target_exit:
                    agent.new_path_needed = True
                    
    def step(self):
        
        self.current_step += 1
        if self.current_step % 10 == 0:
            self.agents_to_evaluate = [agent for agent in self.schedule.agents if isinstance(agent, StudentAgent)]
            self.active_students = len(self.agents_to_evaluate)
            self.evaluate_student_path()
        else:
            self.evaluate_student_path()
            
            # print(self.traffic_at_exits, self.current_step)
        self.schedule.step()
        if self.num_students == 0:
            print("Everyone escaped!")
            pd.DataFrame(DENSITY_MATRIX).to_csv('./analysis/paths/density_matrix.csv')   
            self.running = False

            
    def run_model(self):
        self.step()
