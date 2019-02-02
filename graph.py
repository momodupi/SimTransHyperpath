#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self):
        self.n_dirc = {}

    # add a new node
    def add_node(self, n):
        self.n_dirc.update({n:[]})

    # add a new edge
    def add_edge(self, n1, n2):
        if n1 not in self.n_dirc:
            self.add_node(n1)

        if n2 not in self.n_dirc:
            self.add_node(n2)
        
        self.n_dirc[n1].append(n2)

    def find_edge(self, n1, n2):
        if (n1 not in self.n_dirc) or (n2 not in self.n_dirc):
            return ()
        elif n2 in self.n_dirc[n1]:
            return (n1, n2)
        elif n1 in self.n_dirc[n2]:
            return (n2, n1)
        else:
            return ()

    # remove node with corresponding edges
    def remove_node(self, n):
        for i in self.n_dirc:
            try:
                self.n_dirc[i].remove(n)
            except:
                pass

        try:
            del self.n_dirc[n]
        except KeyError:
            pass

    # print the graph
    def print_graph(self):
        print(self.n_dirc)

    # generate the graph with matrix
    def generate_graph(self, M):
        row, col = M.shape
        if row != col:
            print('matrix error!')
            return
        else:
            for n_r in range(row):
                self.add_node(n_r)
                for n_c in range(col):
                    if M[n_r][n_c] == 1 and n_r != n_c and M[n_c][n_r] != 1:
                        self.add_edge(n_r, n_c)
        self.print_graph()
    
    def generate_random_graph(self, m_size):
        m = np.random.randint(2, size=(m_size, m_size))
        self.generate_graph(m)

    def replace_node(self, n1, rn):
        for i in self.n_dirc:
            self.n_dirc[i] = [ rn if l==n1 else l for l in self.n_dirc[i] ]
        
        self.n_dirc[rn] = self.n_dirc[n1]
        try:
            del self.n_dirc[n1]
        except KeyError:
            pass

        g.print_graph()

g = Graph()
g.generate_random_graph(5)
print(g.find_edge(2,3))
g.replace_node(1,'a')
