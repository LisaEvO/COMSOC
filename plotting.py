import matplotlib.pyplot as plt
from pywaffle import Waffle
import matplotlib as mpl



from voters import *
from parties import *
import networkx as nx

import matplotlib.pyplot as plt
from collections import defaultdict

def plot_spectrum(voters, parties, vcmap=None, pcmap=None, fig_name=None,node_size=30):
    
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
    plt.scatter(parties_x, parties_y, s=node_size, c=pcolors, marker='o', label=party_labels)

    for label, x, y in zip(party_labels, parties_x, parties_y):
        ax.annotate(label, (x, y), textcoords="offset points", xytext=(0,5), ha='center', color=pcmap[label])

    if fig_name!=None:
        plt.savefig(fig_name) 

    plt.show()

def plot_seats_multiple_runs(outcomes, pcmap=None, legend=True, fig_name=None):
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
    if legend == True:
        plt.legend(bbox_to_anchor=(1, 1.05))
    if fig_name!=None:
        plt.savefig(fig_name) 
    plt.show()


def plot_flow_graph(elections, pcmap=None, fig_name = None):
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
    if fig_name!=None:
        plt.savefig(fig_name) 
    plt.show()


def compare_polls(poll_1, poll_2, myelection):
    # amount of parties
    partys = []
    for p in myelection.parties:
        partys.append(p.name)

    # set width of bar 
    barWidth = 0.25
    
    # set height of bar 
    seats_1 = poll_1.values()
    seats_2 = poll_2.values()
    
    # Set position of bar on X axis 
    br1 = np.arange(len(partys)) 
    br2 = [x + barWidth for x in br1] 
    
    # Make the plot
    plt.bar(br1, seats_1, color ='#6bbad6', width = barWidth, label ='first poll') 
    plt.bar(br2, seats_2, color ='#3361ab', width = barWidth, label ='last poll') 
 
    # Adding Xticks 
    plt.xlabel('Parties', fontsize = 15) 
    plt.ylabel('Seats', fontsize = 15) 
    plt.title('Polling resuls')
    plt.xticks([r + barWidth for r in range(len(partys))],partys)

    plt.legend()
    plt.show() 


def check_colourrange(colourrange=str):
    gradient = np.linspace(-1, 1)
    gradient = np.vstack((gradient, gradient))
    colorgrad = plt.imshow(gradient, aspect='auto', cmap=mpl.colormaps[colourrange])

    print(colorgrad)

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def seat_distribution_chart(poll, myelection, colorrange=str):
    seis = mpl.colormaps[colorrange]
    partys = []
    hexs = []

    # ranges
    OldMin, OldMax = -1, 1
    NewMin, NewMax = 0, 256
    OldRange = (OldMax - OldMin)  
    NewRange = (NewMax - NewMin)  


    # getting and converting the values to rgb then hex
    for p in myelection.parties:
        OldValue = (p.position)
        NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
        partys.append(NewValue[0])

    for i in partys:
        colour_rgb = seis(round(i))
        colour_hex = rgb_to_hex(round(colour_rgb[0]*100), round(colour_rgb[1]*100), round(colour_rgb[2]*100))
        hexs.append(colour_hex)

    # plotting the distribution of seats
    data = poll
    fig = plt.figure(
        FigureClass=Waffle, 
        rows=10, 
        values=data, 
        colors=(hexs),
        title={'label': 'Election results', 'loc': 'left', 'color': 'white'},
        labels=["{0} ({1})".format(k, v) for k, v in data.items()],
        alpha=0.3,
        facecolor='black',
        legend={'loc': 'lower left', 'bbox_to_anchor': (1.0, 0.0), 'framealpha': 1}
    )
    # fig.gca().set_facecolor('#EEEEEE')
    fig.set_facecolor('black')
    fig.legend(loc='right')
    plt.show()
