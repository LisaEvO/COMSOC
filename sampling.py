import numpy as np
from scipy import stats

from parties import *
from voters import *


def sample_parties(num_parties, distribution='uniform', dim=1, params=None, representation=False):
    if distribution == 'uniform':
        pass

    if distribution == 'multimodal':
        if params is None:
            params = {'modes': [{'mean': [-0.5, 0.5], 'std': 0.5, 'weight': 0.5}, {'mean': [0.5, -0.5], 'std': 0.5, 'weight': 0.5}]}

        # Ensure that the weights sum to 1
        if abs(sum(mode['weight'] for mode in params['modes']) - 1) > 1e-6:
            raise ValueError("Sum of weights must be equal to 1.")
            pass

        # Randomly choose a mode based on weights (but ensure every cluster is represented at least once if representation==True)
        if representation:
            modes = np.array([i  for i in range(len(params['modes']))])
            modes = np.append(modes, np.random.choice(len(params['modes']), size=(num_parties-len(params['modes']),), p=[mode['weight'] for mode in params['modes']]))

        else:
            modes = np.random.choice(len(params['modes']), size=(num_parties,), p=[mode['weight'] for mode in params['modes']])
            

        # Sample from the selected modes (parties)
        samples = np.zeros((num_parties, dim))
        for i in range(len(params['modes'])):
            mode_indices = np.where(modes == i)[0]
            samples[mode_indices, :] = np.random.normal(loc=params['modes'][i]['mean'], 
                                                        scale=params['modes'][i]['std'], size=(len(mode_indices), dim))
        
        party_positions = samples

        parties = [Party(name=chr(i + 97), idx=i, position = pos) for i, pos in enumerate(sorted(party_positions, key=lambda lr: lr[0]))]

    return parties
        


def sample_voters(demographic, parties, distribution='uniform', dim=1, params=None, shuffle=False):
    num_voters = sum([len(val) for val in demographic.values()])
    if distribution == 'uniform':
        if params is None:
            params = {'low': 0, 'high': 1}
        voter_positions = np.random.uniform(params['low'], params['high'], size=(num_voters, dim))

    elif distribution == 'truncated_normal':
        if params is None:
            params = {'mean': 0, 'std': 1, 'low': -2, 'high': 2}

        # Ensure that the bounds are reasonable
        a, b = (params['low'] - params['mean']) / params['std'], (params['high'] - params['mean']) / params['std']
        voter_positions = stats.truncnorm.rvs(a, b, loc=params['mean'], scale=params['std'], size=(num_voters, dim))

    elif distribution == 'multimodal':
        if params is None:
            params = {'modes': [{'mean': [-0.5, 0.5], 'std': 0.5, 'weight': 0.5}, {'mean': [0.5, -0.5], 'std': 0.5, 'weight': 0.5}]}

        # Ensure that the weights sum to 1
        if abs(sum(mode['weight'] for mode in params['modes']) - 1) > 1e-6:
            raise ValueError("Sum of weights must be equal to 1.")

        # Randomly choose a mode based on weights
        modes = np.random.choice(len(params['modes']), size=(num_voters,), p=[mode['weight'] for mode in params['modes']])

        # Sample from the selected modes (parties)
        samples = np.zeros((num_voters, dim))
        for i in range(len(params['modes'])):
            mode_indices = np.where(modes == i)[0]
            samples[mode_indices, :] = np.random.normal(loc=params['modes'][i]['mean'], 
                                                        scale=params['modes'][i]['std'], size=(len(mode_indices), dim))

        voter_positions = samples
    else:
        raise ValueError("Invalid distribution. Supported distributions are 'uniform', 'truncated_normal', and 'multimodal'.")
    
    #create preferences and voters 
    voters = []
    preferences = []

    for i, voter in enumerate(voter_positions):
        preferences.append(sorted(parties, key = lambda party: np.linalg.norm(voter_positions[i] - party.position)))
    
    if shuffle:
        for preference in preferences:
            for i in range(len(preference) - 1):
                if np.random.rand(1) < 1e-1:
                    preference[i], preference[i+1] = preference[i+1], preference[i]

    
    id = 0
    for voter_type, val in demographic.items():
        for args in val:
            voters.append(voter_type(id, voter_positions[id], preferences[id], *args))
            id += 1
    
    return voters