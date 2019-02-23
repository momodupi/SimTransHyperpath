# SimTrans

## Install
* Python3
* numpy
* matplotlib

## Usage
You can find the manual in [wiki](https://github.com/momodupi/SimTrans/wiki).


| Modules |Description | Arguments | Return |
| -- |-------- | -------- | -- |
|  **SimTrans_Graph** |
| `add_node(n)` | add n as a new node | `n`: node | N/A |
| `add_edge(n1,n2)` | add a new edge between n1 and n2 | `n1`: start node <br> `n2`: end node | N/A |
| `add_w_edge(n1,n2,w)` | add a new edge between n1 and n2 with weight w | `n1`: start node <br> `n2`: end node <br> `w`: edge weight | N/A |
| `update_w_edge(n1,n2,w)` | update weight to the edge (n1,n2) if exists | `n1`: start node <br> `n2`: end node <br> `w`: edge weight | N/A |
| `update_w_all_edges(m_f,m_t,m_c)` | update all edges weight with matrices | `mf`: flow matrix <br> `mt`: cost matrix <br> `mc`: cost matrix | N/A |
| `update_flow(n1,n2,f)` | update flow f for edge (n1,n2) | `n1`: start node <br> `n2`: end node <br> `f`: edge flow | N/A |
| `get_all_nodes()` | return all nodes in the graph | N/A | list of all nodes |
| `get_all_edges()` | return all edges | N/A | list of all edges |
| `get_all_paths(n1,n2)` | get all path from n1 to n2 | `n1`: start node <br> `n2`: end node | list of all paths |
| `get_paths_cost(n1,n2)` | get the cost for each path from n1 to n2 | `n1`: start node <br> `n2`: end node | list of all path cost |
| `get_flow(n1,n2)` | get flow from n1 to n2 | `n1`: start node <br> `n2`: end node | flow of (n1,n2) |
| `remove_node(n)` | remove node n with corresponding edges |
| `remove_edge(n1,n2)` | remove edge (n1,n2) if exists |
| `print_graph()` | print the entire graph | `n1`: start node <br> `n2`: end node | N/A |
| `create_graph(M)` | create a graph with matrix M | `M`: edge matrix | N/A |
| `create_random_graph(ms)` | create a random graph with size | `ms`: number of nodes | N/A |
| **SimTrans_Passenger** |
| `get_decision(n1, n2)` | get passenger decision from n1 to n2 | `n1`: start node <br> `n2`: end node | list of probability distribution over all paths |
| `get_path()` | get the path of this passenger | N/A | selected path |
| `track_position(t)` | track the position of this passenger at time t | `t`: current time | current position |
| **SimTrans_Simulator** |
| `set_mode(mode)` | set the simulator mode | `'normal'`: simulator in normal mode with transfer time, no nomalized flow <br> `'notranstime'`: simulator without transfer time, no nomalized flow <br> `'wardrop'`: simulator without transfer time, nomalized flow for wardrop | N/A |
| `run(s,e,in,sn)` | run simulator | `s`: start time <br> `e`: end time <br> `in`: initial number of passengers <br> `sn`: number of passengers at each step | N/A |
| `plot_edge_flow(n1,n2,s,e)` | plot flow for edge (n1, n2) from time s to e | `n1`: start node <br> `n2`: end node <br> `s`: start time <br> `e`: end time | N/A |
| `plot_all_edges_flow(s,e)` | plot flow for each edges from s_time to e_time | `s`: start time <br> `e`: end time | N/A |
| `plot_all_paths_cost(s,e)` | plot cost of each path from time s to e | `s`: start time <br> `e`: end time | N/A |
| `plot_all_paths_decision(s,e)` | plot decision of each path from time s to e | `s`: start time <br> `e`: end time | N/A |
| `plot_show()` | display all plotted figure | N/A | N/A |



## An example
A simple simulator for a city with 6 nodes and 3 transportation modes.

```python
# Import all required package
from SimTrans_Graph import SimTrans_Graph
from SimTrans_Simulator import SimTrans_Simulator
import numpy as np
```

```python
# Generate graph
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

# create a graph
g.create_graph(g_m)

# update the flow and cost
g.update_w_all_edges(m_f, m_t, m_c)

# set the simulator with graph 
m = SimTrans_Simulator(g, 0, 6)

# initial passengers: 5
# arriving passengers at each time: 5
# running time: 3600
start_time = 0
end_time = 3600
m.set_mode('normal')
m.run(start_time, end_time, 5, 1)

# plot the flow of edges and cost of paths
m.plot_all_edges_flow(start_time, end_time)
m.plot_all_paths_cost(start_time, end_time)
m.plot_all_paths_decision(start_time, end_time)
m.plot_show()
```


