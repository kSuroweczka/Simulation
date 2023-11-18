import mesa
from agents import StudentAgent, Walls
from utils import *

class EvacuationModel(mesa.Model):
    occupaded_cells = set()

    def __init__(self, num_students, width=WIDTH, height=HEIGHT, num_steps=20):
        self.width = width
        self.height = height
        self.num_students = num_students
        self.num_steps = num_steps

        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)

        # use in the futer to optimize students movement
        occupied_cells_by_walls = self.create_walls()

        # Create students
        for i in range(self.num_students):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            while (x, y) in occupied_cells_by_walls:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
            
            pos = (x, y)
            student = StudentAgent(i, self, State.ACTIVE)
            occupied_cells_by_walls.add(pos)
    
            self.grid.place_agent(student, pos)
            self.schedule.add(student)

        self.running = True

    def create_walls(self):
        occupied_cells = set()  # Track occupied cells

        rectangles = [
            ((0, 18), (48, 34)),
            ((49, 26), (96, 42)),
            ((94, 0), (196, 18)),
            ((197, 10), (249, 28)),
            ((26, 35), (30, 43)),
            ((18,44),(40,56)),
            ((226,29),(230,37)),
            ((216,38),(238,50)),
            ((0,96),(48,112)),
            ((148,94),(249,110)),
            ((49,102),(147,119)),
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
                    w = Walls(f'{x}-{y}', self, State.OBSTACLE)
                    self.grid.place_agent(w, pos)
                    self.schedule.add(w)
                    occupied_cells.add(pos)

        return occupied_cells


    def step(self):
        self.schedule.step()

    def run_model(self):
        for i in range(self.num_steps):
            self.step()