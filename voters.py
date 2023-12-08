
import numpy as np
from multiset import *

class Voter(object):
    
    def __init__(self, id, preference):
        self.id = id
        self.true_preference = preference
        self.ballot = preference
    
    def vote(self):
        return self.ballot


class Saint(Voter):

    def __init__(self, id, preference):
        super.__init__(self, id, preference)
    
    def update_ballot(self, poll):
        self.ballot = self.preference


class Spineless(Voter):

    def __init__(self, id, preference):
        super.__init__(self, id, preference)

    def update_ballot(self, poll):
        frontrunner = max(poll.items(), key=lambda item: item[1])[0]
        preference = self.true_preference.copy()
        self.ballot = preference.insert(0, preference.pop(preference.index(frontrunner)))

    
class Opportunist(Voter):

    def __init__(self, id, preference, k):
        super.__init__(self, id, preference)
        self.k = k

    def update_ballot(self, poll):
        topk = self.true_preference[:self.k]
        front_from_topk = max([p for p in poll.items() if p[0] in topk])[0]
        preference = self.true_preference.copy()
        self.ballot = preference.insert(0, preference.pop(preference.index(front_from_topk)))


class Follower(Voter):

    def __init__(self, id, preference, g):
        super.__init__(self, id, preference)
        self.g = g

    def update_ballot(self, poll):
        frontg = [i[0] for i in sorted(poll.items(), key=lambda item: item[1])[-self.g:]]
        top_from_frontg = self.true_preference[min(self.true_preference.index(p) for p in frontg)]
        preference = self.true_preference.copy()
        self.ballot = preference.insert(0, preference.pop(preference.index(top_from_frontg)))

class NonConformist(Voter):

    def __init__(self, id, preference, k):
        super.__init__(self, id, preference)
        self.k = k
    
    def update_ballot(self, poll):
        topk = self.true_preference[:self.k]
        back_from_topk = min([p for p in poll.items() if p[0] in topk])[0]
        preference = self.true_preference.copy()
        self.ballot = preference.insert(0, preference.pop(preference.index(back_from_topk)))

class Strategist(Voter):

    def __init__(self, id, preference, k, g):
        super.__init__(self, id, preference)
        self.k = k
        self.g = g

    def update_ballot(self, poll):
        bottomk = self.true_preference[-self.k:]
        frontg = [i[0] for i in sorted(poll.items(), key=lambda item: item[1])[-self.g:]]

        inbotandfront = [p for p in bottomk if p in frontg]

        if inbotandfront != []:
            topk = self.true_preference[:self.k]
            front_from_topk = max([p for p in poll.items() if p[0] in topk])[0]
            preference = self.true_preference.copy()
            self.ballot = preference.insert(0, preference.pop(preference.index(front_from_topk)))
            
        else:
            self.ballot = self.true_preference
