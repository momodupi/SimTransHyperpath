from SimTrans_Graph import SimTrans_Graph
from SimTrans_Passenger import SimTrans_Passenger
from SimTrans_Simulator import SimTrans_Simulator

import numpy as np

g = SimTrans_Graph()

# a graph with original 0 and destination 6
g_m = np.array([
    [0,1,1,0,0,0,1],
    [0,0,1,1,0,0,0],
    [0,1,0,0,0,1,0],
    [0,0,0,0,1,0,0],
    [0,0,0,0,0,1,1],
    [0,0,0,0,1,0,1],
    [0,0,0,0,0,0,0]
])

# initial flow
m_f = np.zeros((7,7))

# time consumption
m_t = 60*np.array([
    [0,20,5,0,0,0,10],#0
    [0,0,5,20,0,0,0],#1
    [0,5,0,0,0,7,0],#2
    [0,0,0,15,0,0],#3
    [0,0,0,0,0,5,15],#4
    [0,0,0,0,5,0,2],#5
    [0,0,0,0,0,0,0]#6
])

# pecuniary consumption
m_c = np.array([
    [0,2,8,0,0,0,30],#0
    [0,0,0,2,0,0,0],#1
    [0,0,0,0,0,7,0],#2
    [0,0,0,0,2,0,0],#3
    [0,0,0,0,0,0,2],#4
    [0,0,0,0,0,0,8],#5
    [0,0,0,0,0,0,0]#6
])

# create a graph
g.create_graph(g_m)

# update the flow and cost
g.update_w_all_edges(m_f, m_t, m_c)

# set the simulator with graph 
m = SimTrans_Simulator(g, 0, 6)

# initial passengers: 50
# arriving passengers at each time: 50
# running time: 3600
m.run(0, 3600, 5, 5)

# plot the flow of each edge
m.plot_all_edge_flow(0,3600)
m.plot_show()

