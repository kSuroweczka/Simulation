import mesa
from utils import State

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
    def __init__(self, unique_id, model, initial_state=State.SECURITY):
        super().__init__(unique_id, model)
        self.state = initial_state

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

