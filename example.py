from SimTrans_Graph import SimTrans_Graph
from SimTrans_Simulator import SimTrans_Simulator

import numpy as np



def main():
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
    '''
    m_t = np.array([
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
    '''
    
    m_t = np.array([
        [0,1,0.8,0,0,0,0.5],#0
        [0,0,1,1,0,0,0],#1
        [0,1,0,0,0,0.8,0],#2
        [0,0,0,0,1,0,0],#3
        [0,0,0,0,0,1,1],#4
        [0,0,0,0,1,0,0.8],#5
        [0,0,0,0,0,0,0]#6
    ])
    '''
    m_c = np.array([
        [0,0.9,1,0,0,0,4],#0
        [0,0,1,1,0,0,0],#1
        [0,1,0,0,0,1,0],#2
        [0,0,0,0,1,0,0],#3
        [0,0,0,0,0,1,1],#4
        [0,0,0,0,1,0,1],#5
        [0,0,0,0,0,0,0]#6
    ])
    '''
    '''
    m_t = float(1/108)*np.array([
        [0,1,1,0,0,0,1],#0
        [0,0,1,1,0,0,0],#1
        [0,1,0,0,0,1,0],#2
        [0,0,0,0,1,0,0],#3
        [0,0,0,0,0,1,1],#4
        [0,0,0,0,1,0,1],#5
        [0,0,0,0,0,0,0]#6
    ])
    '''
    m_c = np.array([
        [0,20,21,0,0,0,68],#0
        [0,0,5,22,0,0,0],#1
        [0,5,0,0,0,25,0],#2
        [0,0,0,0,17,0,0],#3
        [0,0,0,0,0,5,17],#4
        [0,0,0,0,5,0,22],#5
        [0,0,0,0,0,0,0]#6
    ])
        

    # create a graph
    g.create_graph(g_m)

    # update the flow and cost
    g.update_w_all_edges(m_f, m_t, m_c)


    # set the simulator with graph 
    m = SimTrans_Simulator(g, 0, 6)

    # initial passengers: 5
    # arriving passengers at each time: 1
    # running time: 3600
    # simulator mode: wardrop graph without transit time
    start_time = 0
    end_time = 20
    m.set_mode('wardrop')
    m.run(start_time, end_time, 0, 1)

    #print(g.get_all_paths   (0,6))

    # plot the flow of edges and cost of paths
    m.plot_all_edges_flow(start_time, end_time)
    m.plot_all_paths_cost(start_time, end_time)
    m.plot_all_paths_decision(start_time, end_time)
    m.plot_show()


if __name__ == "__main__":
    main()
