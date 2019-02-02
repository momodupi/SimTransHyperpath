#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class SimTrans(object):
    

    def __init__(self):
        self.n_dirc = {}
        self.n_path = []

    # add a new node
    def add_node(self, n):
        self.n_dirc.update({n:[]})

    def add_subgraph(self, n):
        self.n_dirc.update(n)

    def get_all_nodes(self):
        return [d for d in self.n_dirc]

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

    def remove_edge(self, n1, n2):
        if n2 in self.n_dirc[n1]:
            self.n_dirc[n1].pop(self.n_dirc[n1].index(n2))

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
                    if M[n_r][n_c] == 1 and n_r != n_c:
                        self.add_edge(n_r, n_c)
        self.print_graph()
    
    def generate_complete_tree_graph(self, m_size):
        m = np.ones((m_size, m_size), dtype=int)
        self.generate_graph(m)

    def generate_random_graph(self, m_size):
        m = np.random.randint(2, size=(m_size, m_size))
        self.generate_graph(m)

    def replace_node(self, n1, rn):
        for i in self.n_dirc:
            self.n_dirc[i] = [ rn if l==n1 else l for l in self.n_dirc[i] ]
        if n1 in self.n_dirc:
            self.n_dirc[rn] = self.n_dirc[n1]
            del self.n_dirc[n1]

        self.print_graph()

    def generate_path(self, n1, n2, passed, path): 
        passed[n1]= True
        path.append(n1) 
  
        if n1 == n2:
            self.n_path.append(path[:])
        else:
            for i in self.n_dirc[n1]: 
                if passed[i] == False: 
                    self.generate_path(i, n2, passed, path) 
                      
        path.pop()
        passed[n1]= False
   

    def generate_all_path(self, n1, n2): 
        passed = [ False for i in self.get_all_nodes() ]
        path = [] 
        self.n_path = []
        self.generate_path(n1, n2, passed, path)
        
        for i in self.n_path:
            print(i)


'''
    def generate_all_path(self, n1, n2):
        passed = [ False for i in self.get_all_nodes() ]
        path = []
        p_list = []
        p_list.append(self.generate_path(n1, n2, path, passed))

    def generate_path(self, n1, n2, path, passed):
        passed[n1] = True
        path.append(n1)

        if n1 == n2:
            return path
        if n1 not in self.n_dirc:
            return path
        for n in self.n_dirc[n1]:
            if passed[n] == False: 
                path = self.generate_path(n, n2, path, passed)
        path.pop()
        passed[n1] = False
        return path
'''


g = SimTrans()
g.generate_random_graph(10)
print(g.find_edge(2,3))

#print(g.generate_path(0,3))
g.generate_all_path(1,2)