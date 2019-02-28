#!/usr/bin/env python
# -*- coding: utf-8 -*-

from SimTrans_Graph import SimTrans_Graph
from SimTrans_Passenger import SimTrans_Passenger


import numpy as np
import matplotlib.pyplot as plt



class SimTrans_Simulator(object):
    def __init__(self, g, o, d):
        self.graph = g
        self.ori = o
        self.des = d
        self.edge_flow = {}
        self.edge_flow_history = []
        self.edge_cost_history = []
        self.edge_decision_history = []
        self.p_list = []
        self.conv_cost = 0
        self.plot_num = 0
        self.mode = 'normal'

    def set_mode(self, mode='normal'):
        '''set the simulator mode'''
        self.mode = mode

    def plot_edge_flow(self, n1, n2, s_time, e_time):
        '''plot flow for edge (n1, n2) from s_time to e_time'''
        self.plot_num = self.plot_num + 1
        plt.figure(self.plot_num)
        k = np.arange(s_time,e_time,1)

        plt.plot(k, [ i[(n1,n2)] for i in self.edge_flow_history ], label='{}'.format((n1,n2)))
        #plt.legend(loc='upper right')
        plt.xlabel('time (s)')
        plt.ylabel('Flow')
        plt.title('Flow of edge {}'.format((n1,n2)))
        plt.savefig('edge.png', dpi=600)
        
    def plot_all_edges_flow(self, s_time, e_time):
        '''plot flow for each edges from s_time to e_time'''
        self.plot_num = self.plot_num + 1
        plt.figure(self.plot_num)
        k = np.arange(s_time,e_time,1)

        for e in self.edge_flow:
            plt.plot(k, [ i[e] for i in self.edge_flow_history ], label='{}'.format(e))

        plt.legend(loc='upper right')
        plt.title('Flow of all edges')
        plt.xlabel('time (s)')
        plt.ylabel('Flow')
        plt.savefig('flow.png', dpi=600)

    def plot_all_paths_cost(self, s_time, e_time):
        '''plot cost of each path from s_time to e_time'''
        self.plot_num = self.plot_num + 1
        plt.figure(self.plot_num)
        k = np.arange(s_time,e_time,1)

        for e in self.graph.get_paths_cost(self.ori ,self.des):
            idx = self.graph.get_paths_cost(self.ori ,self.des).index(e)
            plt.plot(k, [ i[ idx ] for i in self.edge_cost_history ], label='{}'.format(self.graph.get_all_paths(self.ori, self.des)[idx]))

        plt.legend(loc='upper right')
        plt.title('Cost of all paths')
        plt.xlabel('time (s)')
        plt.ylabel('Cost')
        plt.savefig('cost.png', dpi=600)

    def plot_all_paths_decision(self, s_time, e_time):
        '''plot decision of each path from s_time to e_time'''
        self.plot_num = self.plot_num + 1
        plt.figure(self.plot_num)
        k = np.arange(s_time,e_time,1)

        for e in self.graph.get_paths_cost(self.ori ,self.des):
            idx = self.graph.get_paths_cost(self.ori ,self.des).index(e)
            plt.plot(k, [ i[ idx ] for i in self.edge_decision_history ], label='{}'.format(self.graph.get_all_paths(self.ori, self.des)[idx]))

        plt.legend(loc='upper right')
        plt.title('Decision for all paths')
        plt.xlabel('time (s)')
        plt.ylabel('Decision')
        plt.savefig('decision.png', dpi=600)

    def plot_show(self):
        '''display all plotted figure'''
        plt.show()

    def simulator_normal(self, s_time, e_time, init_num, step_num):
        '''simulator in normal mode: with transfer time, no nomalized flow'''
        for i in self.graph.get_all_edges():
            for e in i:
                self.edge_flow.update( {(e[0], e[1][0]): self.graph.get_flow(e[0], e[1][0])} )
        print(self.edge_flow)
        
        for i in range(0, init_num):
            self.p_list.append(SimTrans_Passenger(self.graph, self.ori ,self.des, s_time))

        for t in range(0, e_time):
            for i in range(0, step_num):
                self.p_list.append(SimTrans_Passenger(self.graph, self.ori ,self.des, t))

            { self.edge_flow.update( {e_formate: 0} ) for e_formate in self.edge_flow }

            for passenger in self.p_list:
                e = passenger.track_position(t)
                if e in self.edge_flow:
                    self.edge_flow.update( {e: self.edge_flow.get(e)+1} )
                elif e == self.des:
                    self.p_list.remove(passenger)
                    
            for e in self.edge_flow:
                self.graph.update_flow(e[0], e[1], self.edge_flow.get(e))

            
            print('\r\ntime {}:  flow:{}'.format(t, self.edge_flow))
            self.edge_flow_history.append( dict(self.edge_flow) )
            print('cost:{}'.format(self.graph.get_paths_cost(self.ori ,self.des)))
            self.edge_cost_history.append( self.graph.get_paths_cost(self.ori ,self.des) )
            print('decision:{}'.format(self.p_list[-1].get_decision(self.ori ,self.des)))
            self.edge_decision_history.append( self.p_list[-1].get_decision(self.ori ,self.des) )
        
    def simulator_notranstime(self, s_time, e_time, init_num, step_num):
        '''simulator: without transfer time, no nomalized flow'''
        for i in self.graph.get_all_edges():
            for e in i:
                self.edge_flow.update( {(e[0], e[1][0]): self.graph.get_flow(e[0], e[1][0])} )
        print(self.edge_flow)
        
        for i in range(0, init_num):
            self.p_list.append(SimTrans_Passenger(self.graph, self.ori ,self.des, s_time))

        for t in range(0, e_time):
            self.p_list = []
            for i in range(0, step_num):
                self.p_list.append(SimTrans_Passenger(self.graph, self.ori ,self.des, t))

            { self.edge_flow.update( {e_formate: 0} ) for e_formate in self.edge_flow }

            for passenger in self.p_list:
                p_path = passenger.get_path()
                for i in range(0, len(p_path)-1):
                    self.edge_flow.update( {(p_path[i],p_path[i+1]): self.edge_flow.get( (p_path[i],p_path[i+1]) )+1} )
             
            for e in self.edge_flow:
                self.graph.update_flow(e[0], e[1], self.edge_flow.get(e))
            
            print('\r\ntime {}:  flow:{}'.format(t, self.edge_flow))
            self.edge_flow_history.append( dict(self.edge_flow) )
            print('cost:{}'.format(self.graph.get_paths_cost(self.ori ,self.des)))
            self.edge_cost_history.append( self.graph.get_paths_cost(self.ori ,self.des) )
            print('decision:{}'.format(self.p_list[-1].get_decision(self.ori ,self.des)))
            self.edge_decision_history.append( self.p_list[-1].get_decision(self.ori ,self.des) )

    def simulator_wardrop(self, s_time, e_time, init_num, step_num):
        '''simulator: without transfer time, nomalized flow for wardrop'''
        for i in self.graph.get_all_edges():
            for e in i:
                self.edge_flow.update( {(e[0], e[1][0]): self.graph.get_flow(e[0], e[1][0])} )
        print(self.edge_flow)
        
        p = SimTrans_Passenger(self.graph, self.ori ,self.des, s_time)

        for t in range(0, e_time):            
            p = SimTrans_Passenger(self.graph, self.ori ,self.des, s_time)
            flow_list = p.get_decision( self.ori ,self.des )
            
            { self.edge_flow.update( {e_formate: 0} ) for e_formate in self.edge_flow }

            path_list = self.graph.get_all_paths(self.ori, self.des)
            for f in flow_list:
                f_path = path_list[ flow_list.index(f) ]
                for i in range(0, len(f_path)-1):
                    self.edge_flow.update( {(f_path[i],f_path[i+1]): self.edge_flow.get( (f_path[i],f_path[i+1]) )+ f } )
             
            for e in self.edge_flow:
                self.graph.update_flow(e[0], e[1], self.edge_flow.get(e))
            
            print('\r\ntime {}:  flow:{}'.format(t, self.edge_flow))
            self.edge_flow_history.append( dict(self.edge_flow) )
            print('cost:{}'.format(self.graph.get_paths_cost(self.ori ,self.des)))
            self.edge_cost_history.append( self.graph.get_paths_cost(self.ori ,self.des) )
            print('decision:{}'.format(p.get_decision(self.ori ,self.des)))
            self.edge_decision_history.append( p.get_decision(self.ori ,self.des) )
        
        p1 = np.array( p.get_decision(self.ori ,self.des ) )
        p2 = np.array( self.graph.get_paths_cost(self.ori ,self.des) )
        print( p1.dot(p2) )
        self.conv_cost = p1.dot(p2)

    def get_convergence(self):
        return self.conv_cost

    def run_once(self, s_time, e_time, init_num, step_num):
        '''run simulator from s_time to e_time'''
        if self.mode == 'wardrop':
            self.simulator_wardrop(s_time, e_time, init_num, step_num)
        elif self.mode == 'notranstime':
            self.simulator_notranstime(s_time, e_time, init_num, step_num)
        else:
            self.simulator_normal(s_time, e_time, init_num, step_num)


    def run_sensitivity(self, start_time, end_time, m_f, m_t, m_c, edge_list=[], m_t_range=[], m_c_range=1):
        K = 10
        for e in edge_list:
            self.plot_num = self.plot_num + 1
            plt.figure(self.plot_num)
            k = np.arange(m_c[e[0]][e[1]]-K, m_c[e[0]][e[1]]+K)
            for e_m_t in m_t_range:
                c_cost = []
                for e_m_c in range(m_c[e[0]][e[1]]-K, m_c[e[0]][e[1]]+K):
                    self.edge_flow = {}
                    self.edge_flow_history = []
                    self.edge_cost_history = []
                    self.edge_decision_history = []
                    self.p_list = []
                    self.graph.update_w_all_edges(m_f, m_t, m_c)
                    self.graph.update_w_edge(e[0], e[1], self.graph.convert_w_edge(0, e_m_t, e_m_c))
                    #self.SimTrans_Simulator(g, 0, 6)
                    self.set_mode('wardrop')
                    self.run_once(start_time, end_time, 0, 1)
                    c_cost.append(self.get_convergence())

                plt.plot(k, c_cost, label='$a={}$'.format(e_m_t))

            plt.legend(loc='lower right')
            plt.xlabel('b of ({})'.format((e[0], e[1])))
            plt.ylabel('average cost')
            plt.title('Average cost of changing constant cost of {}'.format((e[0], e[1])))
            plt.savefig('avrgcst_{}.png'.format((e[0], e[1])), dpi=600)
            
