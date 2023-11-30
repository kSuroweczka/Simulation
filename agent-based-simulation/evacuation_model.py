import mesa
from agents import StudentAgent, Walls, Exit
from utils import *

class EvacuationModel(mesa.Model):

    def __init__(self, num_students, width=WIDTH, height=HEIGHT, num_steps=20):
        self.width = width
        self.height = height
        self.num_students = num_students
        self.num_steps = num_steps

        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)

        # use in the futer to optimize students movement
        self.walls = self.create_walls()
        self.exits = self.create_exits()
        self.create_students()

        self.running = True
    
    def create_students(self):
        for i in range(self.num_students):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while (x, y) in self.walls or (x, y) in self.exits:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            
            pos = (x, y)
            student = StudentAgent(i, self, pos, State.ACTIVE, self.exits)
    
            self.grid.place_agent(student, pos)
            self.schedule.add(student)


    def create_walls(self):
        walls = {}  # Track occupied cells

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
                    self.grid.place_agent(wall, pos)
                    walls[pos] = wall
        return walls
    
    def create_exits(self):
        exits = {}
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
        return exits
    
    def step(self):
        self.schedule.step()

    def run_model(self):
        for i in range(self.num_steps):
            self.step()