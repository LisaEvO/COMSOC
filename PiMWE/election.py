from collections import Counter
from PiMWE.voters import *

class Election(object):

    def __init__(self, voters:list, parties:list, num_seats:int, num_polls:int, poll_type='parliament'):
        
        self.voters = voters
        self.num_voters = len(self.voters)
        
        self.parties = parties
        self.num_parties = len(self.parties)
        
        self.num_seats = num_seats
        self.num_polls = num_polls

        self.poll_type = poll_type
        self.parliament = Counter({None : self.num_seats})

    def __repr__(self):
        return f'Election({self.num_voters}, {self.num_parties}, {self.num_seats}, {self.num_polls})'
    
    def __str__(self):
        return f'Election with {self.num_voters} voters, {self.num_parties} parties for {self.num_seats} seats'
    
    def aggregate_votes(self, ballots):
        raise NotImplementedError
    
    def elect_parliament(self, votes):
        raise NotImplementedError
    
    def poll(self, parliament,*args):
        if self.poll_type == 'parliament':
            return parliament
        
        elif self.poll_type == 'frontrunner':
            return Counter({p[0] : p[1] for p in parliament.most_common(1)})
        
        elif self.poll_type == 'frontg':
            return Counter({p[0] : p[1] for p in self.parliament.most_common(args[0])})
        
        else:
            raise ValueError('invalid poll_type')
        
    def update_ballots(self, poll_result):
        for voter in self.voters:
            voter.update_ballot(poll_result)


    def run(self):
        
        poll_results = []

        for poll in range(self.num_polls):
            current_ballots = [voter.vote() for voter in self.voters]
            current_votes = self.aggregate_votes(current_ballots)
            poll_result = self.poll(self.elect_parliament(current_votes))
            poll_results.append(poll_result)
            self.update_ballots(poll_result)
            
        
        final_ballots = [voter.vote() for voter in self.voters]
        final_votes = self.aggregate_votes(final_ballots)
        self.parliament = self.elect_parliament(final_votes)
        
        election_results = poll_results + [self.parliament]
        
        return election_results
         
    
class DHondt(Election):
    
    def __init__(self, voters:list, parties:list, num_seats:int, num_polls:int,poll_type='parliament', *args, **kwargs):
        super().__init__(voters, parties, num_seats, num_polls, poll_type, *args, **kwargs)

    def __repr__(self):
        return 'DHondt ' + super().__repr__()
    
    def __str__(self):
        return 'DHondt ' + super().__str__()
    
    def aggregate_votes(self, ballots):
        votes = Counter([ballot[0] for ballot in ballots])
        return votes
    
    def elect_parliament(self, votes):
        seats_so_far = Counter({party : 0 for party in self.parties})
        
        while sum(s for s in seats_so_far.values()) < self.num_seats:
            quot = {party: votes[party] / (seats_so_far[party] + 1) for party in self.parties}
            seats_so_far[max(quot, key=quot.get)] +=1
            
        parliament = seats_so_far
        return parliament
        
        
