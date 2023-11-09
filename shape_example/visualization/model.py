import mesa

class Walls(mesa.Agent):
    def __init__(self,model,pos,a_type):
        super().__init__(pos,model)
        self.pos=pos
        self.type=a_type
 
class Walker(mesa.Agent):
    def __init__(self, unique_id, model, a_type,pos=(0,0)):
        super().__init__(unique_id, model)
        self.a_type = a_type
        
    def step(self):
        self.move()
        
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False
        )
        while True:
            new_pos = self.random.choice(possible_steps)
            if self.model.grid.is_cell_empty(new_pos):
                break
        self.model.grid.move_agent(self, new_pos)




    


class MSModel(mesa.Model):
    def __init__(self, N, width, height):
        self.N = N  # num of agents
        self.grid = mesa.space.SingleGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self.make_agents()
        self.running = True

        
    def make_agents(self):
        occupied_cells = set()  # Track occupied cells
        wall = []

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
                    wall.append((x, y))


        for pos in wall:
            a = Walls(self, pos, "wall")
            self.grid.place_agent(a, (pos[0], pos[1]))
            self.schedule.add(a)
            occupied_cells.add((pos[0], pos[1]))
        
  
        
        for i in range(self.N):
            a=Walker(i, self, "student")
            self.schedule.add(a)
            
            while True:
                x = self.random.randrange(self.grid.width)
                y = self.random.randrange(self.grid.height)
                pos = (x, y)
                if pos not in occupied_cells:
                    occupied_cells.add(pos)
                    break
            self.grid.place_agent(a, pos)
        



    def step(self):
        self.schedule.step()
        

        
