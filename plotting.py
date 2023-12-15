import matplotlib.pyplot as plt

def plot_seats_over_time(results):
    seat_plot = {}
    for result in results:
        for party in result:
            if party.name not in seat_plot:
                seat_plot[party.name]=([result[party]], party.position)
            else:
                seat_plot[party.name][0].append(result[party])
    poll_nrs = range(len(results))
    for p in seat_plot.keys():
        plt.plot(poll_nrs, seat_plot[p][0], label=p+": "+ str(np.round(seat_plot[p][1],2)))
    plt.xlabel("Poll")
    plt.ylabel("Seats")
    plt.xticks(poll_nrs)
    plt.legend(bbox_to_anchor=(1, 1.05))
    plt.show()