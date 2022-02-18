"""
Nodes and Graphing
"""

class Graph:
    """ Graph class, for an undirected, unweighted graph with an adjacency list
        For an edge A-B, it appears in the adjacency list as A-B and B-A """
        
    def __init__(self, V = [], E = []):
        """ Create a new graph from a list of verticies V and edges E. 
            By default, the graph is undirected """
        
        self.G = {}
        
        for v in V:
            self.add_vertex(v)
        for u, v in E:
            self.add_ege(u, v)
    
    def add_vertex(self, v):
        if v not in self.G:
            self.G[v] = set()
    
    def add_edge(self, u, v):
        # add vertices in case they don't already exist
        self.add_vertex(u)
        self.add_vertex(v)
        
        #add undirected edge (u, v)
        self.G[u].add(v)
        self.G[v].add(u)