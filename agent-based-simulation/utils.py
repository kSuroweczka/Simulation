from enum import Enum
import numpy as np

class State(Enum):
    ACTIVE = 1
    ESCAPED = 2
    OBSTACLE = 3
    EXIT = 4

WIDTH = 250
HEIGHT = 120
PIXEL_RATIO = 4

global CELLS_OCCUPIED_BY_STUDENTS
CELLS_OCCUPIED_BY_STUDENTS =[]

global DENSITY_MATRIX
DENSITY_MATRIX = np.zeros((WIDTH, HEIGHT))

MAP_OBJECTS = {
    'WALL': 1,
    'EXIT': 2,
    'BENCH': 3,
    'TREE': 4,
}

EXITS={}

Colors = {
    'STUDENT': "#000080",
    'WALL': "#000000",
    'EXIT': "#d62728",
    'BENCH': "#7d420e",
    'TREE': "#108722", 
}