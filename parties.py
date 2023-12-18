import numpy as np
from voters import *

class Party(object):
    
    def __init__(self, name:str, idx:int, position:np.ndarray):
        self.name = name
        self.idx = idx
        self.position = position
        self.poldeg = 0
    
    def __repr__(self):
        return f'Party({self.name}, {round(self.poldeg, 2)})'

    def __str__(self):
        return f'Party {self.name}'

    def compute_poldeg(self, voters:Voter):
        num_fans = sum([voter.preference[0] == self for voter in voters])
        num_haters = sum([voter.preference[-1] == self for voter in voters])

        self.poldeg = 2 * min(num_fans, num_haters) / len(voters)