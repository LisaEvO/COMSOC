import numpy as np


class Party(object):
    
    def __init__(self, name:str, position:np.ndarray):
        self.name = name
        self.position = position
        self.poldeg = 0
    
    def __repr__(self):
        return f'Party({self.name}, {self.position})'

    def __str__(self):
        return f'Party {self.name}'
