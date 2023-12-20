import mesa
from agents import StudentAgent, Walls, Exit, Bench, Tree
from utils import *

class EvacuationModel(mesa.Model):

    def __init__(self, num_students, width=WIDTH, height=HEIGHT, num_steps=20):
        self.width = width
        self.height = height
        self.num_students = num_students
        self.num_steps = num_steps
        # self.occupied_cells_by_student: list[(int,int)]

        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)

        # use in the future to optimize students movement
        self.walls, self.wall_pos = self.create_walls()
        self.exits,self.inside_exits = self.create_exits()
        self.benches, self.bench_pos = self.create_benches()
        self.trees, self.tree_pos = self.create_trees()
        self.obstacles = self.wall_pos + self.bench_pos + self.tree_pos
        self.create_students()

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
    
            self.grid.place_agent(student, pos)
            self.schedule.add(student)

            student.find_target_exit()   ### after creating students get the target_exit
 

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
        return walls, wall_pos
    
    def create_benches(self):
        benches = {}
        benches_positions = [
            ((119, 30), (119, 31)), 
            ((119, 45), (119, 46)),
            ((119, 60), (119, 61)),
            ((149, 30), (149, 31)),
            ((149, 45), (149, 46)),
            ((149, 60), (149, 61)),
            ((143, 38), (143, 39)),
            ((143, 53), (143, 54)),
            ((70, 65), (71, 65)), # przy boiskach dół
            ((85, 65), (86, 65)), 
            ((100, 65),(101, 65)),
            ((93, 70), (94, 70)), # przy boiskach góra
            ((78, 70), (79, 70)), 
            ((63, 70), (64, 70)),
            ((125, 65), (126, 65)), # środek dół
            ((138, 65), (139, 65)), 
            ((131, 70), (132, 70)), # środek góra
            ((119, 75), (119, 76)), 
            ((119, 85), (119, 86)),
            ((113, 78), (113, 79)), 
            ((113, 88), (113, 89)),
            ((160, 65), (161, 65)), # przy boiskach na flanki góra
            ((170, 65), (171, 65)),
            ((180, 65), (181, 65)),
            ((190, 65), (191, 65)),
            ((160, 40), (161, 40)), # przy boiskach na flanki dół
            ((170, 40), (171, 40)),
            ((180, 40), (181, 40)),
            ((170, 84), (171, 84)), # góra
            ((180, 84), (181, 84)),
            ((190, 84), (191, 84)),
            ((165, 78), (165, 79)),
            ((165, 72), (165, 73)),
            ((195, 78), (195, 79)),
            ((149, 80), (149, 81)), # góra przy wyjściu
        ]

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
        trees_positions = [
            (101, 70),
            (86, 70),
            (71, 70),
            (110, 50),
            (80, 52),
            (64, 60),
            (112, 42),
            (134, 76),
            (121, 64),
            (130, 54),
            (135, 58),
            (127, 60),
            (155, 54),
            (154, 48)

        ]

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
    
    def step(self):
        self.schedule.step()

    def run_model(self):
        for i in range(self.num_steps):
            self.step()