import mesa
from utils import State

class Exit(mesa.Agent):    
    def __init__(self, unique_id, model, state=State.EXIT):
        super().__init__(unique_id, model)
        self.state = state
        self.escaped_students = 0

class Walls(mesa.Agent):
    def __init__(self, unique_id, model, state=State.OBSTACLE):
        super().__init__(unique_id, model)
        self.state = state

class StudentAgent(mesa.Agent):
    def __init__(self, unique_id, model, position: (int, int), initial_state=State.ACTIVE):
        super().__init__(unique_id, model)
        self.state = initial_state
        self.position = position
        self.target_exit: Exit = None

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

        is_not_occupied = self.model.grid.get_cell_list_contents([new_position]) == 0
        if is_not_occupied:
            self.model.grid.move_agent(self, new_position)

    def step(self):
        self.move()


