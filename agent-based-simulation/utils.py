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

EXITS={}


Colors = {
    'STUDENT': "#000080",
    'WALL': "#000000",
    'EXIT': "#d62728",
    'BENCH': "#7d420e",
    'TREE': "#108722", 
}

Trees = [
            (101, 73),
            (88, 74),
            (71, 73),
            (86, 83),
            (108, 82),
            (109, 92),
            (94, 90),
            (100, 93),

            (71, 50),
            (78, 48),
            (85, 60),
            (90, 57),
            (110, 60),
            (109, 48),
            (107, 30),
            (105, 33),
            (103, 31),
            (123, 55),

            (133, 48),
            (132, 52),
            (130, 30),
            (135, 28),
            (140, 60),

            (130, 82),
            (128, 88),
            (135, 87),
            (140, 80),

            (160, 85),
            (170, 87),
            (180, 87),
            (192, 86),
            (215, 80),

            (155, 52),
            (154, 45),

            (162, 25),
            (210, 32),
            (212, 37),
            (180, 32),
            (185, 28)

        ]

Benches = [
            ((119, 30), (119, 31)),  # wejście od luny - git

            ((149, 30), (149, 31)), # wejście od studenciaka prawa - git
            ((149, 45), (149, 46)),
            ((149, 60), (149, 61)),
            ((149, 38), (149, 39)),
            ((149, 53), (149, 54)),

            ((143, 38), (143, 39)), # wejście od studenciaka lewa - git
            ((143, 52), (143, 53)),
            ((143, 59), (143, 60)),

            ((70, 70), (71, 70)), # przy boiskach góra - git
            ((77, 70), (78, 70)), 
            ((84, 70),(85, 70)),
            ((91, 70), (92, 70)), 
            ((98, 70),(99, 70)),

            ((101, 65), (102, 65)), # przy boiskach dół - git
            ((94, 65), (95, 65)), 
            ((87, 65), (88, 65)),
            ((80, 65), (81, 65)), 
            ((73, 65), (74, 65)),

            ((125, 65), (126, 65)), # środek dół - git
            ((138, 65), (139, 65)), 
            ((131, 65), (132, 65)),

            ((120, 70), (121, 70)), # środek góra - git
            ((124, 70), (125, 70)),
            ((134, 70), (135, 70)),
            ((141, 70), (142, 70)),

            ((119, 75), (119, 76)), # wyjście paczkomat prawa - git
            ((119, 88), (119, 89)),
            ((119, 92), (119, 93)),

            ((113, 72), (113, 73)), # wyjście paczkomat lewa - git
            ((113, 76), (113, 77)),
            ((113, 82), (113, 83)),
            ((113, 87), (113, 88)),
            ((113, 92), (113, 93)),

            ((154, 65), (155, 65)), # przy boiskach na flanki góra - git
            ((160, 65), (161, 65)), 
            ((170, 65), (171, 65)),
            ((180, 65), (181, 65)),
            ((190, 65), (191, 65)),

            ((160, 45), (161, 45)), # przy boiskach na flanki dół - git
            ((170, 45), (171, 45)),
            ((180, 45), (181, 45)),

            ((200, 50), (201, 50)), # przy boiskach na flanki dół prawo - git
            ((204, 50), (205, 50)),
            ((209, 50), (210, 50)),

            ((195, 32), (195, 33)),

            ((170, 84), (171, 84)), # góra przy filutku - git
            ((180, 84), (181, 84)),
            ((190, 84), (191, 84)),
            ((200, 84), (201, 84)),
            
            ((201, 72), (201, 73)), # przy filutku prawo - git

            ((165, 78), (165, 79)), # przy filutku lewo - git
            ((165, 72), (165, 73)),
            ((165, 83), (165, 84)),

            ((149, 74), (149, 75)), # góra przy wyjściu - git

            ((143, 73), (143, 74)), # wejście od good looda lewa - git
            ((143, 78), (143, 79)),
            ((143, 83), (143, 84)),
            ((143, 88), (143, 89)),

            ((149, 70), (150, 70)), # git
            ((154, 70), (155, 70)),
            ((160, 70), (161, 70)),

            ((122, 93), (140, 93)),

            ((122, 86),(122,86)), # środek góra skos lewa - git
            ((123, 85),(123,85)),

            ((124, 81),(124,81)),
            ((125, 80),(125,80)),

            ((126, 76),(126,76)),
            ((127, 75),(127,75)),

            
            ((138, 86),(138,86)),  # środek góra skos prawa - git
            ((137, 85),(137,85)),

            ((136, 81),(136,81)),
            ((135, 80),(135,80)),

            ((134, 76),(134,76)),
            ((133, 75),(133,75)),

            
            ((133, 62),(133,62)), # środek dół skos prawo
            ((134, 61),(134,61)),

            ((135, 53),(135,53)),
            ((136, 52),(136,52)),

            ((137, 45),(137,45)),
            ((138, 44),(138,44)),


            ((130, 62),(130,62)), # środek dół skos lewo
            ((129, 61),(129,61)),

            ((126, 53),(126,53)),
            ((125, 52),(125,52)),

            ((124, 45),(124,45)),
            ((123, 44),(123,44)),
        ]


