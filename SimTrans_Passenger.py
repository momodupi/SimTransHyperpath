#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class SimTrans_Passenger(object):
    def __init__(self, g, o, d, time):
        self.graph = g
        self.ori = o
        self.des = d
        self.s_time = time

        self.path, self.t_time = self.select_path()
        self.pos = [0, self.path[1]]

        self.t_time = [0] + self.t_time
        for i in range(1, len(self.t_time)):
            self.t_time[i] = self.t_time[i-1]+self.t_time[i]
        
    # decision mode
    def get_decision(self, n1, n2):
        c_list = self.graph.get_paths_cost(n1, n2)
        #d_list = [ float(i/sum(c_list)) for i in c_list ]
        #print(d_list)
        c_list = [ np.exp(-i) for i in c_list ]
        return [ float( i/sum(c_list)) for i in c_list ]

    # select path based on decision mode
    def select_path(self):
        dec_set = self.get_decision(self.ori, self.des)
        num_path = self.graph.get_all_paths(self.ori, self.des)
        sel = np.random.choice(len(num_path), 1, p = dec_set)

        time_list = []
        for i in range(0,len(num_path[sel[0]])-1):
            time_list.append( self.graph.get_edge( num_path[sel[0]][i], num_path[sel[0]][i+1] )[1][1].get('time') )

        return num_path[sel[0]], time_list

    # track the position of passenger
    def track_position(self, c_t):
        for t_edge in self.t_time:
            if (c_t - self.s_time) <= t_edge:
                n1 = self.path[ self.t_time.index(t_edge) - 1 ]
                n2 = self.path[ self.t_time.index(t_edge) ]
                self.pos = (n1, n2)
                #print(self.pos)
                break
            elif (c_t - self.s_time) > self.t_time[-1]:
                self.pos = self.des
                #print(self.pos)
        return self.pos

