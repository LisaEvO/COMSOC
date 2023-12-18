from collections import Counter
import numpy as np

class Voter(object):
    
    def __init__(self, id:int, position:np.ndarray, preference:list, *args, **kwargs):
        self.id = id
        self.position = position
        self.preference = preference
        self.ballot = self.preference
        
    def __repr__(self):
        return f'Voter {self.id}: pref = {self.preference[0]}, vote = {self.ballot[0]}'

    def __str__(self):
        return f'Voter {self.id} with preference: {self.preference} and current vote: {self.ballot[0]}'
    
    def update_ballot(self, poll_result:Counter):
        raise NotImplementedError
    
    def vote(self):
        return self.ballot


class Saint(Voter):

    def __init__(self, id, position, preference, *args, **kwargs):
        super().__init__(id, position, preference)
    
    def __repr__(self):
        return super().__repr__() + ' (Saint)'
    
    def __str__(self):
        return 'Saint ' + super().__str__()
    
    def update_ballot(self, poll_result):
        self.ballot = self.preference


class Spineless(Voter):

    def __init__(self, id, position, preference, *args, **kwargs):
        super().__init__(id, position, preference)
    
    def __repr__(self):
        return super().__repr__() + ' (Spineless)'
    
    def __str__(self):
        return 'Spineless ' + super().__str__()

    def update_ballot(self, poll_result):
        frontrunner = [p[0] for p in poll_result.most_common(1)][0]
        preference = self.preference.copy()
        preference.insert(0, preference.pop(preference.index(frontrunner)))

        self.ballot = preference
        
   
class Opportunist(Voter):

    def __init__(self, id, position, preference, k:int, *args, **kwargs):
        super().__init__(id, position, preference)
        self.k = k

    def __repr__(self):
        return super().__repr__() + f' (Opportunist({self.k}))'

    def __str__(self):
        return f'Opportunist({self.k}) ' + super().__str__()
    
    def update_ballot(self, poll_result):
        topk = self.preference[:self.k]
        front_from_topk = max([p for p in poll_result.items() if p[0] in topk], key=lambda p: p[1])[0]
        preference = self.preference.copy()
        preference.insert(0, preference.pop(preference.index(front_from_topk)))

        self.ballot = preference

class Follower(Voter):

    def __init__(self, id, position, preference, g:int, *args, **kwargs):
        super().__init__(id, position, preference)
        self.g = g

    def __repr__(self):
        return super().__repr__() + f' (Follower({self.g}))'
    
    def __str__(self):
        return f'Follower({self.g}) ' + super().__str__()

    def update_ballot(self, poll_result):
        frontg = [p[0] for p in poll_result.most_common(self.g)]
        top_from_frontg = self.preference[min(self.preference.index(p) for p in frontg)]
        preference = self.preference.copy()
        preference.insert(0, preference.pop(preference.index(top_from_frontg)))

        self.ballot = preference


class NonConformist(Voter):

    def __init__(self, id, position, preference, k, *args, **kwargs):
        super().__init__(id, position, preference)
        self.k = k
    
    def __repr__(self):
        return super().__repr__() + f' (NonConformist({self.k}))'
    
    def __str__(self):
        return f'NonConformist({self.k}) ' + super().__str__()
    
    def update_ballot(self, poll_result):
        topk = self.preference[:self.k]
        back_from_topk = min([p for p in poll_result.items() if p[0] in topk], key=lambda p: p[1])[0]
        preference = self.preference.copy()
        preference.insert(0, preference.pop(preference.index(back_from_topk)))

        self.ballot = preference
                       

class Strategist(Voter):

    def __init__(self, id, position, preference, k, g, *args, **kwargs):
        super().__init__(id, position, preference)
        self.k = k
        self.g = g

    def __repr__(self):
        return super().__repr__() + f' (Strategist({self.k}, {self.g}))'
    
    def __str__(self):
        return f'Strategist({self.k}, {self.g}) ' + super().__str__()
    
    def update_ballot(self, poll_result):
        bottomk = self.preference[-self.k:]
        frontg = [p[0] for p in poll_result.most_common(self.g)]

        inbotandfront = [p for p in bottomk if p in frontg]

        if inbotandfront != []:
            topk = self.preference[:self.k]
            front_from_topk = max([p for p in poll_result.items() if p[0] in topk], key=lambda p: p[1])[0]
            preference = self.preference.copy()
            preference.insert(0, preference.pop(preference.index(front_from_topk)))

            self.ballot = preference
            
        else:
            self.ballot = self.preference
