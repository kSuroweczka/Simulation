import mesa
from agents import StudentAgent, Walls, Exit, Bench, Tree
from utils import *
import pandas as pd
import json

 
class EvacuationModel(mesa.Model):

    def __init__(self, num_students, move_probability, width=WIDTH, height=HEIGHT, num_steps=80):
        self.width = width
        self.height = height
        self.num_students = num_students
        self.num_steps = num_steps
        self.buffer_update_interval = 5
        self.current_step = 0
        self.move_probability = move_probability

        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)

        self.traffic_at_exits = self.calculate_traffic_for_all_exits()
        self.walls, self.wall_pos, self.exits, self.inside_exits, self.benches, self.bench_pos, self.trees, self.tree_pos = self.create_map()

        self.obstacles = self.wall_pos + self.bench_pos + self.tree_pos
        self.create_students()
        self.step_count = 0
        self.running = True

    def create_students(self):
        for i in range(self.num_students):
            x = self.random.randrange(10, 230)
            y = self.random.randrange(30, 100)
            while (x, y) in self.obstacles or (x, y) in self.exits:
                x = self.random.randrange(10, 230)
                y = self.random.randrange(30, 100)
            
            pos = (x, y)
            student = StudentAgent(i, self, pos, State.ACTIVE, obstacles=self.obstacles, exits=self.inside_exits) #### potem zmienic exits i walls na cos z model
            DENSITY_MATRIX[x][y] += 1

            self.grid.place_agent(student, pos)
            self.schedule.add(student)

            student.find_target_exit()   ### after creating students get the target_exit

        df = pd.DataFrame([EXITS])
        df.to_csv("../agent-based-simulation/analysis/exits/exits.csv")


    def create_map(self):
        with open('./map_template.csv', 'r'):
            df = pd.read_csv('./map_template.csv', sep=',', header=0, index_col=0)
            data = df.values
            data = data.transpose()
        
        walls = {}
        wall_pos = []
        trees = {}
        benches = {}
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
                    walls[pos] = wall
                elif data[y][x] == 2:
                    pos = (x, y)
                    exit = Exit(f'{x}-exit-{y}', self, pos, State.EXIT)
                    self.grid.place_agent(exit, pos)
                    exits[pos] = exit
                elif data[y][x] == 3:
                    pos = (x, y)
                    bench = Bench(f'{x}-bench-{y}', self, pos, State.OBSTACLE)
                    self.grid.place_agent(bench, pos)
                    benches[pos] = bench
                elif data[y][x] == 4:
                    pos = (x, y)
                    tree = Tree(f'{x}-tree-{y}', self, pos, State.OBSTACLE)
                    self.grid.place_agent(tree, pos)
                    trees[pos] = tree
                
        return walls, wall_pos, exits, inside_exits, benches, list(benches.keys()),  trees, list(trees.keys()) 
        
    
    def calculate_traffic_for_all_exits(self):
        traffic_at_exits = {}
        exits_pos =  [(96,23), 
                (96,22),
                (117,18),      
                (145,18), 
                (145,97),
                (115,106),]
        
        for exit in exits_pos:
            buffer_size = 10
            area = self.grid.get_neighborhood(exit, moore=True, include_center=True, radius=buffer_size)
            agents = self.grid.get_cell_list_contents(area)
            count = sum(1 for agent in agents if isinstance(agent, StudentAgent))
            traffic_at_exits[exit] = count
        return traffic_at_exits
    
    
    def step(self):
        self.current_step += 1
        if self.current_step % 10 == 0:
            self.traffic_at_exits = self.calculate_traffic_for_all_exits()
            # print(self.traffic_at_exits, self.current_step)
        self.schedule.step()
        if self.num_students == 0:
            print("Everyone escaped!")
            pd.DataFrame(DENSITY_MATRIX).to_csv('./analysis/paths/density_matrix.csv')   
            self.running = False

            
    def run_model(self):
        self.step()
