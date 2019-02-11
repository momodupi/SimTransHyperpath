from SimTrans_Graph import SimTrans_Graph
from SimTrans_Passenger import SimTrans_Passenger

class SimTrans_Simulator(object):
    def __init__(self, g, o, d):
        self.graph = g
        self.ori = o
        self.des = d
        self.s_time = 0
        self.edge_flow = {}
        self.p_list = []


    def run(self, time, init_num, step_num):
        for i in self.graph.get_all_edges():
            for e in i:
                self.edge_flow.update( {(e[0], e[1][0]): self.graph.get_flow(e[0], e[1][0])} )
        print(self.edge_flow)

        
        for i in range(0, init_num):
            self.p_list.append(SimTrans_Passenger(self.graph, self.ori ,self.des, self.s_time))

        for t in range(0, time):
            for i in range(0, step_num):
                self.p_list.append(SimTrans_Passenger(self.graph, self.ori ,self.des, t))

            { self.edge_flow.update( {e_formate: 0} ) for e_formate in self.edge_flow }

            for passenger in self.p_list:
                e = passenger.track_position(t)
                if e in self.edge_flow:
                    self.edge_flow.update( {e: self.edge_flow.get(e)+1} )
                    #print(self.edge_flow.get(e))
                    #print(self.graph.get_edge(e[0],e[1]))
                elif e == self.des:
                    self.p_list.remove(passenger)
                    
            for e in self.edge_flow:
                self.graph.update_flow(e[0], e[1], self.edge_flow.get(e))


            print('\r\ntime {}:  flow:{}'.format(t, self.edge_flow))
            print('cost:{}'.format(self.graph.get_paths_cost(self.ori ,self.des)))
                
            

