import mesa
from agents import StudentAgent, Walls, Exit, Bench, Tree
from utils import *
import pandas as pd
import json

 
class EvacuationModel(mesa.Model):

    def __init__(self, num_students, width=WIDTH, height=HEIGHT, num_steps=80):
        self.width = width
        self.height = height
        self.num_students = num_students
        self.num_steps = num_steps
        self.buffer_update_interval = 5
        self.current_step = 0
        # self.occupied_cells_by_student: list[(int,int)]

        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)

        self.traffic_at_exits = self.calculate_traffic_for_all_exits()
        self.walls, self.wall_pos = self.create_walls()
        self.exits,self.inside_exits = self.create_exits()
        self.benches, self.bench_pos = self.create_benches()
        self.trees, self.tree_pos = self.create_trees()
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

    def create_walls(self):
        walls = {}  # Track occupied cells
        wall_pos = []

        rectangles = [
            ((0, 18), (48, 34)), # straszny dwór?
            ((49, 26), (96, 42)), 
            ((94, 0), (113, 18)), # luna kebab
            ((118, 0),(143, 18)), # studenciak
            ((148, 0),(196, 18)), # hajduczek
            ((197, 10), (249, 28)), # omega
            ((26, 35), (30, 43)),
            ((18,44),(40,56)),
            ((226,29),(230,37)),
            ((216,38),(238,50)),
            ((0,96),(48,112)),
            ((148,94),(249,110)),
            ((49,102),(113,119)), # bratek
            ((118,102),(143,119)), # good lood
            ((226,85),(230,93)),
            ((220,73),(242,84)),
            ((62,93),(66,101)),
            ((56,81),(78,92)),
            ((0,35),(0,95)),
            ((249,29),(249,93))
        ]

        for top_left, bottom_right in rectangles:
            for x in range(top_left[0], bottom_right[0] + 1):
                for y in range(top_left[1], bottom_right[1] + 1):
                    pos = (x, y)
                    wall = Walls(f'{x}-{y}', self, pos, State.OBSTACLE)
                    wall_pos.append(pos)
                    self.grid.place_agent(wall, pos)
                    walls[pos] = wall
        rrr=  [(x,43) for x in range(49,97)] + [(97,y) for y in range(26, 43)] ## 1,2 sciany przy lewym dolnym wyjsciu
        www =  [(114, y) for y in range(3,18)] + [(117, y) for y in range(3,18)] ### 3,4 sciany srodkowym dolnym wujsciu
        ooo = [(144,y) for y in range(3,19)] + [(147, y) for y in range(3,19)]+[(x,19) for x in range(148,196)]  ## 9,10,14  przy prawym dolnym wyjsciu

        nnn = [(114, y) for y in range(102, 116)] +[(117, y) for y in range(102, 116)]+[(x,101) for x in range(67,114)]  ### 5,6,7 przy lewym gornym wyjsciu
        ttt = [(x,101) for x in range(118,144)] + [(144, y) for y in range(101,107)] + [(147, y) for y in range(95, 107)] + [(x, 93) for x in range(148, 226)]  ###8, 11, 12, 13 przy prawym gornym wyjsciu

        hhh = [(x,57) for x in range(18,41)] + [(17, y) for y in range(44, 57)] ## 15,16 przy lewym dolnym budynku w srodku
        jjj= [(x,95) for x in range(1,49)] + [(55,y) for y in range(81, 92)] # 17,18 przy lewym gornym budynku w srodku
        # wall_pos = wall_pos + rrr + www + ooo + nnn + ttt + hhh + jjj

        return walls, wall_pos
    
    def create_benches(self):
        benches = {}
        benches_positions = Benches

        for top_left, bottom_right in benches_positions:
            for x in range(top_left[0], bottom_right[0] + 1):
                for y in range(top_left[1], bottom_right[1] + 1):
                    pos = (x, y)
                    bench = Bench(f'{x}-bench-{y}', self, pos, State.OBSTACLE)
                    self.grid.place_agent(bench, pos)
                    benches[pos] = bench
        return benches, list(benches.keys())
    
    def create_trees(self):
        trees = {}
        trees_positions = Trees

        for x, y in trees_positions:
            pos = (x, y)
            tree = Tree(f'{x}-tree-{y}', self, pos, State.OBSTACLE)
            self.grid.place_agent(tree, pos)
            trees[pos] = tree
        return trees, list(trees.keys())
    
    def create_exits(self):
        exits = {}

        inside_exits = {(96,19),(96,20),(96,21),(96,22),(96,23), (96,24),(96,25),
                        (114,2),(115,2),(116,2),(117,2),
                        (144,2),(145,2),(146,2),(147,2),
                        (114,117), (115,117),(116,117),(117,117),
                        (144,108),(145,108),(146,108),(147,108)}
        exits_positions = [ 
            ((94, 19), (96, 25)),
            ((114, 0), (117, 2)),
            ((144, 0), (147, 2)), 
            ((144, 108),(147, 110)),
            ((114, 117),(117, 119))
        ]
        
        for top_left, bottom_right in exits_positions:
            for x in range(top_left[0], bottom_right[0] + 1):
                for y in range(top_left[1], bottom_right[1] + 1):
                    pos = (x, y)
                    exit = Exit(f'{x}-exit-{y}', self, pos, State.EXIT)
                    self.grid.place_agent(exit, pos)
                    exits[pos] = exit
        return exits, inside_exits
 
    
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
        print(self.num_students)
        if self.num_students == 0:
            print("Everyone escaped!")
            print(DENSITY_MATRIX.shape)
            pd.DataFrame(DENSITY_MATRIX).to_csv('./analysis/paths/density_matrix.csv')   
            self.running = False

            
    def run_model(self):
        self.step()
