from PiMWE.voters import *
from PiMWE.parties import *
import networkx as nx

import matplotlib.pyplot as plt
from collections import defaultdict

def plot_spectrum(voters, parties, vcmap=None, pcmap=None, node_size=100, annotate=False, fig_name=None):
    
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
    
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    ax.set_xticklabels('')
    ax.set_yticklabels('')
    plt.scatter(voters_x, voters_y, s=0.2, color=vcolors)
    for party in parties:
        plt.scatter(parties_x[party.idx], parties_y[party.idx], s=node_size, color=pcolors[party.idx], marker='o', label=party.name)

    if annotate:
        for label, x, y in zip(party_labels, parties_x, parties_y):
            ax.annotate(label, (x, y), textcoords="offset points", xytext=(0,5), ha='center', color=pcmap[label], fontweight='bold')
    
    else:
        plt.legend()

    if fig_name!=None:
        plt.savefig(fig_name) 
    
    plt.show()

def plot_seats_over_time(outcomes, pcmap=None, legend=False, fig_name=None):
    parties = sorted(list(outcomes[0][0].keys()), key=lambda party: party.idx)
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
        plt.plot(poll_nrs, means[party.name], label=party.name, color=pcolors[i])
        plt.fill_between(poll_nrs, means[party.name]-stds[party.name], 
                         means[party.name]+stds[party.name], alpha=0.2, color = pcolors[i])
    plt.xlabel("Poll")
    plt.ylabel("Seats")
    plt.xticks(poll_nrs)
    
    if legend:
        plt.legend()#bbox_to_anchor=(1, 1.05)
    
    if fig_name !=None:
        plt.savefig(fig_name)

    plt.show()

def plot_flow_graph(elections, pcmap=None, fig_name=None):
    lst_flow_dict, lst_number_fans = [],[]
    for election in elections:
        flow_dict = defaultdict(int)
        number_fans = {party: 0 for party in elections[0].parties}
        for voter in election.voters:
            key = (voter.preference[0], voter.ballot[0])
            flow_dict[key] += 1
            number_fans[voter.ballot[0]] += 1
        lst_flow_dict.append(flow_dict)
        lst_number_fans.append(number_fans)

    flow_dict = {key: [i[key] for i in lst_flow_dict] for key in lst_flow_dict[0]}
    number_fans = {key: [i[key] for i in lst_number_fans] for key in lst_number_fans[0]}

    flow_dict = {key: np.mean(flow_dict[key]) for key in flow_dict}
    number_fans = {key: np.mean(number_fans[key]) for key in number_fans}

    G = nx.DiGraph() 
    for party in number_fans.keys():
        G.add_node(party.name)

    for connection in flow_dict.keys():
        if connection[0]!=connection[1]:
            G.add_edge(connection[0].name,connection[1].name, length = flow_dict[connection])
    
    if pcmap is None:
        cmap = plt.get_cmap('rainbow_r')
        norm = plt.Normalize(0, election.num_parties - 1)
        colors = cmap(norm(np.arange(election.num_parties)))
        pcmap = {party: colors[i] for i, party in enumerate(election.parties)}

    pcolors = [pcmap[party] for party in number_fans.keys()]
    width = [edge[2]['length']/100 for edge in G.edges(data=True)]
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, connectionstyle='arc3, rad = 0.1', 
            node_size=list(number_fans.values()), width=width, node_color=pcolors )
    if fig_name != None:
        plt.savefig(fig_name)
    plt.show()
