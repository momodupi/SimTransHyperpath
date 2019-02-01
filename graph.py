#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, direction=False):
        self.n_dirc = {}
        self.direction = direction

    # add a new node
    def add_node(self, n):
        self.n_dirc.update({n:[]})

    def add_edge(self, n1, n2):
        if n1 not in self.n_dirc:
            self.add_node(n1)

        if n2 not in self.n_dirc:
            self.add_node(n2)
        
        self.n_dirc[n1].append(n2)

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

    def print_graph(self):
        print(self.n_dirc)

