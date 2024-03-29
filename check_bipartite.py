# Alejandro Martos Ayala
# Estructura de datos Final Proyect
'''A bipartite graph is a graph whose vertices can be divided into two disjoint sets so that every edge connects two vertices from different sets
(i.e. there are no edges which connect vertices from the same set). These sets are usually called sides.'''
import numpy as np
import queue
import time
import sys
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self):
        # dictionary containing keys that map to the corresponding vertex object
        self.vertices = {}
 
    def add_vertex(self, key):
        #"""Add a vertex with the given key to the graph."""
        vertex = Vertex(key)
        self.vertices[key] = vertex
 
    def get_vertex(self, key):
        #"""Return vertex object with the corresponding key."""
        return self.vertices[key]
 
    def __contains__(self, key):
        return key in self.vertices
 
    def add_edge(self, src_key, dest_key, weight=1):
        #"""Add edge from src_key to dest_key with given weight."""
        self.vertices[src_key].add_neighbour(self.vertices[dest_key], weight)
 
    def add_undirected_edge(self, v1_key, v2_key, weight=1):
        #"""Add undirected edge (2 directed edges) between v1_key and v2_key with
        #given weight."""
        self.add_edge(v1_key, v2_key, weight)
        self.add_edge(v2_key, v1_key, weight)
 
    def does_undirected_edge_exist(self, v1_key, v2_key):
        #"""Return True if there is an undirected edge between v1_key and v2_key."""
        return (self.does_edge_exist(v1_key, v2_key)
                and self.does_edge_exist(v1_key, v2_key))
 
    def does_edge_exist(self, src_key, dest_key):
        #"""Return True if there is an edge from src_key to dest_key."""
        return self.vertices[src_key].does_it_point_to(self.vertices[dest_key])
 
    def __iter__(self):
        return iter(self.vertices.values())
 
 
class Vertex:
    def __init__(self, key):
        self.key = key
        self.points_to = {}
 
    def get_key(self):
        #"""Return key corresponding to this vertex object."""
        return self.key
 
    def add_neighbour(self, dest, weight):
        #"""Make this vertex point to dest with given edge weight."""
        self.points_to[dest] = weight
 
    def get_neighbours(self):
        #"""Return all vertices pointed to by this vertex."""
        return self.points_to.keys()
 
    def get_weight(self, dest):
        #"""Get weight of edge from this vertex to dest."""
        return self.points_to[dest]
 
    def does_it_point_to(self, dest):
        #"""Return True if this vertex points to dest."""
        return dest in self.points_to
 
 
def is_bipartite(vertex, visited):
    #"""Return True if component containing vertex is bipartite and put all
    #vertices in its component in set visited."""
    colour = {vertex: 0}
    return is_bipartite_helper(vertex, visited, colour)
 
 
def is_bipartite_helper(v, visited, colour):
    #"""Return True if component containing vertex is bipartite and put all
    #vertices in its component in set visited. Uses dictionary colour to keep
    #track of colour of each vertex."""
    visited.add(v)
    next_colour = 1 - colour[v] # switch colour
    for dest in v.get_neighbours():
        if dest not in visited:
            colour[dest] = next_colour
            if not is_bipartite_helper(dest, visited, colour):
                return False
        else:
            if colour[dest] != next_colour:
                return False
    return True

def draw_graph(graph, labelsList):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    labels = {k:k for k in labelsList}    
    

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)
    nx.draw_networkx_labels(G,pos, labels)

    # show graph
    plt.show()

# draw example


 
 
g = Graph()

print('Undirected Graph')
print('Menu')
print('add vertex <key>')
print('add edge <vertex1> <vertex2>')
print('bipartite')
print('display')
print('quit')

# Keep a loop going for menu until user inputs key word 'quit'
while True:
    

    # call the split method to split the input everywhere there is a space
    do = input('What would you like to do? ').split()
    

    # get the first index of that list of the input
    operation = do[0]
    # in both cases of adding vertex or edge the first word must be 'add'
    if operation == 'add':
        suboperation = do[1]
        if suboperation == 'vertex':
            key = do[2]
            if key not in g:
                g.add_vertex(key)
            else:
                print('Vertex already exists.')
        elif suboperation == 'edge':
            v1 = do[2]
            v2 = do[3]
            if v1 not in g:
                print('Vertex {} does not exist.'.format(v1))
            elif v2 not in g:
                print('Vertex {} does not exist.'.format(v2))
            else:
                if not g.does_undirected_edge_exist(v1, v2):
                    g.add_undirected_edge(v1, v2)
                else:
                    print('Edge already exists.')
 
    elif operation == 'bipartite':
        bipartite = True
        visited = set()
        for v in g:
            if v not in visited:
                if not is_bipartite(v, visited):
                    bipartite = False
                    break
 
        if bipartite:
            print('Graph is bipartite.')
        else:
            print('Graph is not bipartite.')
 
    elif operation == 'display':
        print('Vertices: ', end='')
        ForLabels = []
        for v in g:
##            print(v)
            print(v.get_key(), end=' ')
            ForLabels.append(v.get_key())
        print()
 
        print('Edges: ')
        X = []
        Y = []
        for v in g:
            for dest in v.get_neighbours():
##                print(dest)
##                print(dest.get_key())
                x = v.get_key()
                X.append(x)
                y = dest.get_key()
                Y.append(y)
                list_c = [(a, b) for a, b in zip(X, Y)]
                

                
                w = v.get_weight(dest)
                print('(src={}, dest={})'.format(v.get_key(),dest.get_key()))
                                                          
        print()
        draw_graph(list_c, ForLabels)
 
    elif operation == 'quit':
        break
