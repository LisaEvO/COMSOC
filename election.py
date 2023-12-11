import numpy as np
from scipy import stats
from collections import Counter
from voters import *
from parties import Party

class Election(object):

    def __init__(self, voter_composition, num_parties:int, num_seats:int, num_polls:int, pdistr=stats.uniform, vdistr=stats.uniform, ddim=1):
        
        self.voter_composition = voter_composition
        self.num_voters = sum([len(val) for val in self.voter_composition.values()])
        self.num_parties = num_parties
        self.num_seats = num_seats
        self.num_polls = num_polls
        
        self.pdistr = pdistr
        self.vdistr = vdistr
        self.ddim = ddim

        self.voters = self.num_voters * [None]
        self.parties = self.num_parties * [None]
        self.parlement = Counter({None : self.num_seats})


    def __repr__(self):
        return f'Election({self.num_voters}, {self.num_parties}, {self.num_seats}, {self.voter_types})'
    
    def __str__(self):
        return f'Election with {self.num_voters} voters, {self.num_parties} parties for {self.num_seats} seats'
    
    def sample_parties(self):
        party_positions = sorted(self.pdistr.rvs(-1, 2, size=(self.num_parties, self.ddim)), key=lambda lr: lr[0])
        self.parties = [Party(name=chr(i + 97), position=pos) for i, pos in enumerate(party_positions)]
    
    def create_electorate(self):
        id=0
        for voter_type, val in self.voter_composition.items():
            for args in val:
                self.voters[id] = voter_type(id, [None], *args)
                id+=1

    def distribute_voters(self):
        voter_positions = self.vdistr.rvs(-1,2, size=(self.num_voters, self.ddim))
        for i, voter in enumerate(self.voters):
            preference = sorted(self.parties, key = lambda party: np.linalg.norm(voter_positions[i] - party.position))
            voter.preference = preference
          
    def aggregate_votes(self, ballots):
        raise NotImplementedError
    
    def elect_parlement(self, votes):
        raise NotImplementedError
    
    def update_voter_beliefs(self, poll_result):
        for voter in self.voters:
            voter.update_ballot(poll_result)

    def run(self):
        self.sample_parties()
        self.create_electorate()
        self.distribute_voters()
        
        for poll in range(self.num_polls):
            ballots = [voter.vote() for voter in self.voters]
            votes = self.aggregate_votes(ballots)
            poll_result = self.elect_parlement(votes)

            self.update_voter_beliefs(poll_result)
        
        ballots = [voter.vote() for voter in self.voters]
        votes = self.aggregate_votes(ballots)
        election_result = self.elect_parlement(votes)
    
        return election_result
    
class DHondt(Election):
    
    def __init__(self, num_voters, num_parties, num_seats):
        super().__init__(num_voters, num_parties, num_seats)

    def __repr__(self):
        return 'DHondt ' + super().__repr__()
    
    def __str__(self):
        return 'DHondt ' + super().__str__()
    
    def aggregate_votes(self, ballots):
        votes = Counter([ballot[0] for ballot in ballots])
        return votes
    
    def elect_parlement(self, votes):
        #TODO: Meggie
        raise NotImplementedError
        
