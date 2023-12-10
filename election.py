import numpy as np
from scipy import stats
from multiset import *
from voters import *
from parties import Party

class Election(object):

    def __init__(self, num_voters, num_parties, num_seats):
        
        self.num_voters = num_voters
        self.num_parties = num_parties
        self.num_seats = num_seats

        self.voters = self.num_voters * [None]
        self.parties = self.num_parties * [None]
        self.parlement = Multiset({None : self.num_seats})

    def __repr__(self):
        return f'Election({self.num_voters}, {self.num_parties}, {self.num_seats}, {self.voter_types})'
    
    def __str__(self):
        return f'Election with {self.num_voters} voters, {self.num_parties} parties for {self.num_seats} seats'
    
    def sample_parties(self, distr=stats.uniform, dim=1):
        positions = sorted(distr.rvs(-1, 1, size=(self.num_parties, dim)), key=lambda lr: lr[0])
        self.parties = [Party(name=chr(i + 97), position=pos) for i, pos in enumerate(positions)]

    def distribute_voters(self):
        for voter in self.voters:
            favorite = np.random.choice(self.parties)
            preference = sorted(self.parties, key = lambda party: np.linalg.norm(party.position - favorite.position))
            voter.preference = preference
          
    def count_votes(self):
        raise NotImplementedError
    
    def elect_parlement(self):
        pass
    
    def run(self):
        self.sample_parties()
        self.distribute_voters()

    

class DHondt(Election):
    
    def __init__(self, num_voters, num_parties, num_seats):
        super().__init__(num_voters, num_parties, num_seats)

    def count_votes(self):
        pass

    def __repr__(self):
        return 'DHondt ' + super().__repr__()
    
    def __str__(self):
        return 'DHondt ' + super().__str__()
