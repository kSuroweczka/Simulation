import mesa
from agents import StudentAgent, JaguarAgent
from utils import State

def get_num_banned_students(model):
    banned_students = [a for a in model.schedule.agents if a.state == State.BANNED]
    return len(banned_students)

class EvacuationModel(mesa.Model):
    def __init__(self, num_jaguars, num_students, proc_illegal_students, width=20, height=20, num_steps=20):
        self.width = width
        self.height = height
        self.num_jaguars = num_jaguars
        self.num_students = num_students
        self.num_illegal_students = int(num_students * (proc_illegal_students/100))
        self.num_steps = num_steps

        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.datacollector = mesa.DataCollector(
            model_reporters={"Banned Students": get_num_banned_students},
            agent_reporters={"State": lambda x: x.state}
        )

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

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()

    def run_model(self):
        for i in range(self.num_steps):
            self.step()