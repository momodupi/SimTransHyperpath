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

        self.plot_num = 0

    # plot flow for edge (n1, n2)
    def plot_edge_flow(self, n1, n2, s_time, e_time):
        self.plot_num = self.plot_num + 1
        plt.figure(self.plot_num)
        k = np.arange(s_time,e_time,1)
        #flow_plot = np.zeros(e_time-s_time)

        #for i in range(len(self.edge_flow_history)):
            #flow_plot[i] = self.edge_flow_history[i][(n1,n2)]

        plt.plot(k, [ i[(n1,n2)] for i in self.edge_flow_history ], label='{}'.format((n1,n2)))
        #plt.legend(loc='upper right')
        plt.xlabel('time (s)')
        plt.ylabel('Flow')
        plt.title('Flow of edge {}'.format((n1,n2)))
        #plt.show()
        
    # plot flow for each edges
    def plot_all_edges_flow(self, s_time, e_time):
        self.plot_num = self.plot_num + 1
        plt.figure(self.plot_num)
        k = np.arange(s_time,e_time,1)

        for e in self.edge_flow:
            plt.plot(k, [ i[e] for i in self.edge_flow_history ], label='{}'.format(e))

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=int(len(self.edge_flow)/2))
        plt.title('Flow of all edges')
        plt.xlabel('time (s)')
        plt.ylabel('Flow')
        #plt.show()


    # plot cost of each path
    def plot_all_paths_cost(self, s_time, e_time):
        self.plot_num = self.plot_num + 1
        plt.figure(self.plot_num)
        k = np.arange(s_time,e_time,1)

        for e in self.graph.get_paths_cost(self.ori ,self.des):
            idx = self.graph.get_paths_cost(self.ori ,self.des).index(e)
            plt.plot(k, [ i[ idx ] for i in self.edge_cost_history ], label='{}'.format(self.graph.get_all_paths(self.ori, self.des)[idx]))

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=int(len(self.edge_flow)/2))
        plt.title('Cost of all paths')
        plt.xlabel('time (s)')
        plt.ylabel('Cost')
        #plt.show()

    # plot decision of each path
    def plot_all_paths_decision(self, s_time, e_time):
        self.plot_num = self.plot_num + 1
        plt.figure(self.plot_num)
        k = np.arange(s_time,e_time,1)

        for e in self.graph.get_paths_cost(self.ori ,self.des):
            idx = self.graph.get_paths_cost(self.ori ,self.des).index(e)
            plt.plot(k, [ i[ idx ] for i in self.edge_decision_history ], label='{}'.format(self.graph.get_all_paths(self.ori, self.des)[idx]))

        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=int(len(self.edge_flow)/2))
        plt.title('Decision for all paths')
        plt.xlabel('time (s)')
        plt.ylabel('Decision')
        #plt.show()

    
    # display all figure
    def plot_show(self):
        plt.show()

    def run(self, s_time, e_time, init_num, step_num):
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
         
            
