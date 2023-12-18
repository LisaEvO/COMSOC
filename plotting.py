from voters import *
from parties import *
import networkx as nx

import matplotlib.pyplot as plt
from collections import defaultdict

def plot_spectrum(voters, parties, vcmap=None, pcmap=None):
    
    voters_x, voters_y = [voter.position[0] for voter in voters], [voter.position[1] for voter in voters]
    parties_x, parties_y = [party.position[0] for party in parties], [party.position[1] for party in parties]
    party_labels = [party.name for party in parties]
    
    if vcmap is None:
        vcmap = {Saint:'black', Spineless:'black', Follower:'black', Opportunist:'black', NonConformist:'black', Strategist:'black'}
    
    if pcmap is None:
        cmap = plt.get_cmap('rainbow_r')
        norm = plt.Normalize(0, len(parties) - 1)
        colors = cmap(norm(np.arange(len(parties))))
        pcmap = {party.name: colors[i] for i, party in enumerate(parties)}

    vcolors = [vcmap[type(voter)] for voter in voters]
    pcolors = [pcmap[party.name] for party in parties]
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    ax.spines['bottom'].set_position(('axes',0.5))
    ax.spines['left'].set_position(('axes', 0.5))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    ax.set_xticklabels('')
    ax.set_yticklabels('')
    plt.scatter(voters_x, voters_y, s=0.2, color=vcolors)
    plt.scatter(parties_x, parties_y, s=30, c=pcolors, marker='o', label=party_labels)

    for label, x, y in zip(party_labels, parties_x, parties_y):
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(0,5), ha='center', color=pcmap[label])

    plt.show()

def plot_seats_multiple_runs(outcomes, pcmap=None):
    parties = sorted(list(outcomes[0][0].keys()), key=lambda party: party.name)
    data = []
    for outcome in outcomes:
        seat_plot = {}
        for poll in outcome:
            for party in poll:
                if party.name not in seat_plot:
                    seat_plot[party.name]=[poll[party]]
                else:
                    seat_plot[party.name].append(poll[party])
        data.append(seat_plot)
    poll_nrs = range(len(outcome))
    means = {}
    stds = {}

    if pcmap is None:
        cmap = plt.get_cmap('rainbow_r')
        norm = plt.Normalize(0, len(parties) - 1)
        colors = cmap(norm(np.arange(len(parties))))
        pcmap = {party.name: colors[i] for i, party in enumerate(parties)}
    pcolors = [pcmap[party.name] for party in parties]

    for i, party in enumerate(parties):
        means[party.name] = np.mean([d[party.name] for d in data], axis=0)
        stds[party.name] = np.std([d[party.name] for d in data], axis=0)
        plt.plot(poll_nrs, means[party.name], label=party.name+": "+ str(np.round(party.position,2)), color=pcolors[i])
        plt.fill_between(poll_nrs, means[party.name]-stds[party.name], 
                         means[party.name]+stds[party.name], alpha=0.2, color = pcolors[i])
    plt.xlabel("Poll")
    plt.ylabel("Seats")
    plt.xticks(poll_nrs)
    plt.legend(bbox_to_anchor=(1, 1.05))
    plt.show()


def plot_flow_graph(election, pcmap=None):
    flow_dict = defaultdict(int)
    number_fans = defaultdict(int)
    for voter in election.voters:
        key = voter.preference[0].name + voter.ballot[0].name
        flow_dict[key] += 1
        number_fans[voter.ballot[0].name] += 1

    G = nx.DiGraph() 
    for party in number_fans.keys():
        G.add_node(party)

    width  = []
    for connection in flow_dict.keys():
        if connection[0]!=connection[1]:
            G.add_edge(connection[0],connection[1])
            width.append(flow_dict[connection]/100)
    
    if pcmap is None:
        cmap = plt.get_cmap('rainbow_r')
        norm = plt.Normalize(0, election.num_parties - 1)
        colors = cmap(norm(np.arange(election.num_parties)))
        pcmap = {party.name: colors[i] for i, party in enumerate(election.parties)}

    pcolors = [pcmap[party] for party in number_fans.keys()]
            

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1', 
            node_size=list(number_fans.values()), width=width, node_color=pcolors )
    
    plt.show()
