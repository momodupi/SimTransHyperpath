#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class SimTrans_Graph(object):
    def __init__(self):
        self.n_dirc = {}
        self.n_path = []
        self.n_node = []
        self.n_edge = []

    # add a new node
    def add_node(self, n):
        self.n_dirc.update({n:[]})

    # return all added nodes
    def get_all_nodes(self):
        self.n_node = [d for d in self.n_dirc]
        return self.n_node

    # add a new edge
    def add_edge(self, n1, n2):
        if n1 not in self.n_dirc:
            self.add_node(n1)
        if n2 not in self.n_dirc:
            self.add_node(n2)
        self.n_dirc[n1].append((n2,()))

    # add a new weighted edge
    def add_w_edge(self, n1, n2, w):
        if n1 not in self.n_dirc:
            self.add_node(n1)
        if n2 not in self.n_dirc:
            self.add_node(n2)
        if n2 not in self.n_dirc[n1]:
            self.n_dirc[n1].append((n2,w))

    # update weight to an edge if exist
    def update_w_edge(self, n1, n2, w):
        self.remove_edge(n1, n2)
        self.add_w_edge(n1, n2, w)

    # convert edge flow, time, cost into dictionary
    def convert_w_edge(self, m_f=0, m_t=0, m_c=0):
        return {"cost": self.convert_cost(m_f, m_t, m_c) ,"flow": m_f,"time": m_t,"fee": m_c}

    # conver all edges weighe with matrices
    def update_w_all_edges(self, m_f, m_t, m_c):
        #e_s = np.array(self.n_edge).flatten('F')
        for n_list in self.n_edge:
            for e_list in n_list:
                i = e_list[0]
                j = e_list[1][0]
                self.update_w_edge(i, j, self.convert_w_edge(m_f[i][j], m_t[i][j], m_c[i][j]))

    # return an edge if exists
    def get_edge(self, n1, n2):
        if (n1 not in self.n_dirc) or (n2 not in self.n_dirc):
            return ()
        else:
            for e in self.n_dirc[n1]:
                if e[0] == n2:
                    return (n1,e)

    # return all edges
    def get_all_edges(self):
        self.n_edge = []
        for i in self.n_dirc:
            e = [ (i,d) for d in self.n_dirc[i] ]
            self.n_edge.append(e)
        return self.n_edge


    # remove node with corresponding edges
    def remove_node(self, n):
        for i in self.n_dirc:
            self.n_dirc[i] = [i for i in self.n_dirc[i] if i[0] != n]
        try:
            del self.n_dirc[n]
        except KeyError:
            pass

    # remove an edge if exists
    def remove_edge(self, n1, n2):
        self.n_dirc[n1] = [i for i in self.n_dirc[n1] if i[0] != n2]

    # print the entire graph
    def print_graph(self):
        print("Graph: ")
        for i in self.n_dirc:
            print("node{}: {}".format(int(i), self.n_dirc[i]))


    # create a graph with matrix
    def create_graph(self, M):
        row, col = M.shape
        if row != col:
            print('error matrix input!')
            return
        else:
            for n_r in range(row):
                self.add_node(n_r)
                for n_c in range(col):
                    if M[n_r][n_c] == 1 and n_r != n_c:
                        self.add_w_edge(n_r, n_c, 0)
        self.get_all_nodes()
        self.get_all_edges()
        self.print_graph()
    
    # generate a complete graph with size
    def create_complete_tree_graph(self, m_size):
        self.create_graph(np.ones( (m_size, m_size), dtype=int) )

    # create a random graph with size
    def create_random_graph(self, m_size):
        self.create_graph( np.random.randint(2, size=(m_size, m_size)) )


    # get a path
    def get_path(self, n1, n2, passed, path): 
        passed[n1]= True
        path.append(n1)
  
        if n1 == n2:
            self.n_path.append(path[:])
        else:
            for i in self.n_dirc[n1]: 
                n = i[0]
                if passed[n] == False: 
                    #passed[n]= True
                    #path.append( self.get_edge(n1,n) )
                    self.get_path(n, n2, passed, path) 
        path.pop()     
        passed[n1]= False
   
    # get all path
    def get_all_paths(self, n1, n2): 
        passed = [ False for i in self.get_all_nodes() ]
        path = [] 
        self.n_path = []
        self.get_path(n1, n2, passed, path)
        return self.n_path
    
    # get the cost for each path
    def get_paths_cost(self, n1, n2):
        p = self.get_all_paths(n1, n2)
        w_list = []
        for p_list in p:
            w_c = 0
            for i in range(0,len(p_list)-1):
                w_c = w_c + self.get_edge( p_list[i], p_list[i+1] )[1][1].get('cost')
            w_list.append(w_c)
        return w_list
      
    # cost function
    def convert_cost(self, m_f, m_t, m_c):
        # define the cost function
        # i,e. quadritic cost
        return m_c + m_t + 0.5*(m_f*m_f)
    
    # update flow
    def update_flow(self, n1, n2, f):
        e = self.get_edge(n1, n2)
        e[1][1].update({'flow': f})
        e[1][1].update({'cost': self.convert_cost( e[1][1].get('flow'), e[1][1].get('time'), e[1][1].get('fee') )})
        self.update_w_edge(n1, n2, e[1][1])


    # get flow
    def get_flow(self, n1, n2):
        return self.get_edge(n1, n2)[1][1].get('flow')
