import numpy as np
from scipy import stats
from collections import Counter
from voters import *
from parties import Party

class Election(object):

    def __init__(self, voter_composition, num_parties:int, num_seats:int, num_polls:int, 
                 pdistr='uniform', vdistr='truncnorm', ddim=1):
        
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
        if self.pdistr == 'uniform':
            party_positions = sorted(stats.uniform.rvs(-1, 2, size=(self.num_parties, self.ddim)), key=lambda lr: lr[0])
        
        elif self.pidstr == 'truncnorm':
            party_positions = sorted(stats.truncnorm.rvs(-1, 1, size=(self.num_parties, self.ddim)), key=lambda lr: lr[0])
        
        self.parties = [Party(name=chr(i + 97), position=pos) for i, pos in enumerate(party_positions)]
    
    def sample_voters(self):
        if self.vdistr == 'uniform':
            voter_positions = stats.uniform.rvs(-1,2, size=(self.num_voters, self.ddim))

        elif self.vdistr == 'truncnorm':
            voter_positions = stats.truncnorm.rvs(-1,1, size=(self.num_voters, self.ddim))

        preferences = []
        for i, voter in enumerate(self.voters):
            preferences.append( sorted(self.parties, key = lambda party: np.linalg.norm(voter_positions[i] - party.position)))
        
        id = 0
        for voter_type, val in self.voter_composition.items():
            for args in val:
                self.voters[id] = voter_type(id, preferences[id], *args)
                id += 1

   
    def aggregate_votes(self, ballots):
        raise NotImplementedError
    
    def elect_parlement(self, votes):
        raise NotImplementedError
    
    def poll(self, parlement, poll_type='parlement', *args, **kwargs):
        if poll_type == 'parlement':
            return parlement
        
        elif poll_type == 'frontrunner':
            return Counter({p[0] : p[1] for p in parlement.most_common(1)})
        
        elif poll_type == 'frontg':
            return Counter({p[0] : p[1] for p in self.parlement.most_common(args[0])})
        
        else:
            raise ValueError('invalid poll_type')
        
    def update_voter_beliefs(self, poll_result):
        for voter in self.voters:
            voter.update_ballot(poll_result)

    def run(self):
        
        self.sample_parties()
        self.sample_voters()
        
        poll_results = []

        for poll in range(self.num_polls):
            current_ballots = [voter.vote() for voter in self.voters]
            current_votes = self.aggregate_votes(current_ballots)
            poll_result = self.poll(self.elect_parlement(current_votes))
            poll_results.append(poll_result)
            self.update_voter_beliefs(poll_result)
        
        final_ballots = [voter.vote() for voter in self.voters]
        final_votes = self.aggregate_votes(final_ballots)
        self.parlement = self.elect_parlement(final_votes)
        
        election_results = poll_results + [self.parlement]
        
        return election_results
         
    
class DHondt(Election):
    
    def __init__(self, voter_composition, num_parties:int, num_seats:int, num_polls:int, *args, **kwargs):
        super().__init__(voter_composition, num_parties, num_seats, num_polls, *args, **kwargs)

    def __repr__(self):
        return 'DHondt ' + super().__repr__()
    
    def __str__(self):
        return 'DHondt ' + super().__str__()
    
    def aggregate_votes(self, ballots):
        votes = Counter([ballot[0] for ballot in ballots])
        return votes
    
    def elect_parlement(self, votes):
        seats_so_far = Counter({party : 0 for party in self.parties})
        
        while sum(s for s in seats_so_far.values()) < self.num_seats:
            quot = {party: votes[party] / (seats_so_far[party] + 1) for party in self.parties}
            seats_so_far[max(quot, key=quot.get)] +=1
            
        parlement = seats_so_far
        return parlement
        
        
