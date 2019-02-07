from SimTrans_Graph import SimTrans_Graph

import numpy as np

g = SimTrans_Graph()


g_m = np.zeros((7,7))
g_m[0,:]=np.array([0,1,1,0,0,0,1])
g_m[1,:]=np.array([0,0,1,1,0,0,0])
g_m[2,:]=np.array([0,1,1,0,0,1,0])
g_m[3,:]=np.array([0,0,0,0,1,0,0])
g_m[4,:]=np.array([0,0,0,0,0,1,1])
g_m[5,:]=np.array([0,0,0,0,1,0,1])
g_m[6,:]=np.array([0,0,0,0,0,0,0])


w_m = np.zeros((7,7))
#g.create_random_graph(10)
g.create_graph(g_m, w_m)

g.get_all_paths(0,6)

#g.update_w_edge(0,1,g.convert_w_edge(5,4,3))


g.update_w_all_edges(g_m, g_m, g_m)

#g.print_graph()

print(g.get_all_edges())
