from multiset import *

class Voter(object):
    
    def __init__(self, id:int, preference:list, *args, **kwargs):
        self.id = id
        self.preference = preference
        self.ballot = preference
    
    def __repr__(self):
        return f'Voter {self.id}: pref = {self.preference[0]}, vote = {self.ballot[0]}'

    def __str__(self):
        return f'Voter {self.id} with preference: {self.preference} and current vote: {self.ballot[0]}'
    
    def update_ballot(self, poll):
        raise NotImplementedError
    
    def vote(self):
        return self.ballot


class Saint(Voter):

    def __init__(self, id, preference, *args, **kwargs):
        super().__init__(id, preference)
    
    def __repr__(self):
        return super().__repr__() + ' (Saint)'
    
    def __str__(self):
        return 'Saint ' + super().__str__()
    
    def update_ballot(self, poll):
        self.ballot = self.preference


class Spineless(Voter):

    def __init__(self, id, preference, *args, **kwargs):
        super().__init__(id, preference)
    
    def __repr__(self):
        return super().__repr__() + ' (Spineless)'
    
    def __str__(self):
        return 'Spineless ' + super().__str__()

    def update_ballot(self, poll):
        frontrunner = max(poll.items(), key=lambda item: item[1])[0]
        preference = self.preference.copy()
        self.ballot = preference.insert(0, preference.pop(preference.index(frontrunner)))

    
class Opportunist(Voter):

    def __init__(self, id, preference, k, *args, **kwargs):
        super().__init__(id, preference)
        self.k = k

    def __repr__(self):
        return super().__repr__() + f' (Opportunist({self.k}))'

    def __str__(self):
        return f'Opportunist({self.k}) ' + super().__str__()
    
    def update_ballot(self, poll):
        topk = self.preference[:self.k]
        front_from_topk = max([p for p in poll.items() if p[0] in topk])[0]
        preference = self.preference.copy()
        self.ballot = preference.insert(0, preference.pop(preference.index(front_from_topk)))


class Follower(Voter):

    def __init__(self, id, preference, g, *args, **kwargs):
        super().__init__(id, preference)
        self.g = g

    def __repr__(self):
        return super().__repr__() + f' (Follower({self.g}))'
    
    def __str__(self):
        return f'Follower({self.g}) ' + super().__str__()

    def update_ballot(self, poll):
        frontg = [i[0] for i in sorted(poll.items(), key=lambda item: item[1])[-self.g:]]
        top_from_frontg = self.preference[min(self.preference.index(p) for p in frontg)]
        preference = self.preference.copy()
        self.ballot = preference.insert(0, preference.pop(preference.index(top_from_frontg)))


class NonConformist(Voter):

    def __init__(self, id, preference, k, *args, **kwargs):
        super().__init__(id, preference)
        self.k = k
    
    def __repr__(self):
        return super().__repr__() + f' (NonConformist({self.k}))'
    
    def __str__(self):
        return f'NonConformist({self.k}) ' + super().__str__()
    
    def update_ballot(self, poll):
        topk = self.preference[:self.k]
        back_from_topk = min([p for p in poll.items() if p[0] in topk])[0]
        preference = self.preference.copy()
        self.ballot = preference.insert(0, preference.pop(preference.index(back_from_topk)))

class Strategist(Voter):

    def __init__(self, id, preference, k, g, *args, **kwargs):
        super().__init__(id, preference)
        self.k = k
        self.g = g

    def __repr__(self):
        return super().__repr__() + f' (Strategist({self.k}, {self.g}))'
    
    def __str__(self):
        return f'Strategist({self.k}, {self.g}) ' + super().__str__()
    
    def update_ballot(self, poll):
        bottomk = self.preference[-self.k:]
        frontg = [i[0] for i in sorted(poll.items(), key=lambda item: item[1])[-self.g:]]

        inbotandfront = [p for p in bottomk if p in frontg]

        if inbotandfront != []:
            topk = self.preference[:self.k]
            front_from_topk = max([p for p in poll.items() if p[0] in topk])[0]
            preference = self.preference.copy()
            self.ballot = preference.insert(0, preference.pop(preference.index(front_from_topk)))
            
        else:
            self.ballot = self.preference
