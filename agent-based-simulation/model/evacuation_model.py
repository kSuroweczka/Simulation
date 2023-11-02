import mesa
import seaborn as sns
import numpy as np
import pandas as pd

from enum import Enum

class State(Enum):
    LEGAL = 1
    ILLEGAL = 2
    BANNED = 3

class StudentAgent(mesa.Agent):
    def __init__(self, unique_id, model, initial_state, is_legal):
        super().__init__(unique_id, model)

        self.state = initial_state
        self.is_legal = is_legal

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        print(f"Hi, I'm a student nr.{self.unique_id} and I'm {self.state}!")
        self.move()

class JaguarAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def ban(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        students = [obj for obj in cellmates if isinstance(obj, StudentAgent)]
        for student in students:
            if student.state == State.ILLEGAL and self.random.random() < 0.3:
                student.state = State.BANNED

    def step(self):
        print(f"Hi, I'm a jaguar nr.{self.unique_id}! ")
        self.move()
        self.ban()


class EvacuationModel(mesa.Model):
    def __init__(self, width, height, num_jaguars, num_students, proc_illegal_students):
        self.width = width
        self.height = height
        self.num_jaguars = num_jaguars
        self.num_students = num_students
        self.num_illegal_students = int(num_students * proc_illegal_students)

        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)
        # self.running = True

        # Create jaguars
        for i in range(self.num_jaguars):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            jaguar = JaguarAgent(i, self)
            
            self.grid.place_agent(jaguar, (x, y))
            self.schedule.add(jaguar)

        # Create students
        for i in range(self.num_students):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if i < self.num_illegal_students:
                student = StudentAgent(i + num_jaguars, self, State.ILLEGAL, True)
            else:
                student = StudentAgent(i + num_jaguars, self, State.LEGAL, False)
            
            self.grid.place_agent(student, (x, y))
            self.schedule.add(student)

    def step(self):
        self.schedule.step()