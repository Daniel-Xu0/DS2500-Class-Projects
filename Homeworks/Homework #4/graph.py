"""
graph_simplified.py: A graph object for undirected unweighted graphs.

NOTE:

    A simple unweighted undirected graph.
    No visualization, or advanced functions
    but you can print a representation.

"""



class Graph:
    """Graph class, for an undirected, unweighted graph with an adjacency list representation
        For an edge A-B, it appears in the adjaency list as A-B and B-A
    """

    def __init__(self, V = [], E = []):
        """ Create a new graph from a list of verticies V and edges E.
        By default, the graph is undirected """
        self.G = {}

        for v in V:
            self.add_vertex(v)
        for u, v in E:
            self.add_edge(u, v)
            
    def add_vertex(self, v):
        if v not in self.G:
            self.G[v] = set()
        
    def add_edge(self, u, v):
        # add vertices in case they don't already exist
        self.add_vertex(u)
        self.add_vertex(v)

        # add undirected edge (u,v)
        self.G[u].add(v)
        self.G[v].add(u)

    def remove_edge(self, u, v):
        """ Implement this to support unfriend in SocialNetwork """
        pass

    def __getitem__(self, v):
        """ Return all vertices adjacent to v (overriding index operator!)"""
        return self.G.get(v, set())

    def __repr__(self):
        graph_str = ''
        for v in self.G:
            graph_str += '['+v+'] => ' + str(self[v]) + '\n'
        return graph_str

    def is_adjacent(self,u,v):
        """ Test if u and v are adjacent """
        return v in self[u] and u in self[v]
    
    def get_vertices(self):
        """ Get a list of all vertices in the graph """
        return list(self.G.keys())

    def get_edges(self):
        """ Return a list of edges in the graph.  Each edge is a tuple (u,v) """
        edges = []
        for u in self.G:
            for v in self.G[u]:
                edges.append((u,v))
        return edges

    def num_vertices(self):
        """ Return the number of vertices in the graph """
        return len(self.G)

    def num_edges(self):
        """ Return the number of edges in the undirected graph """

        total = 0
        for v in self.G:
            total += self.deg(v)

        return total // 2

    def deg(self,v):
        """ What is the degree of vertext v?  i.e., how many 
        other vertices are adjacent """
        return len(self[v])






def main():
    V = list("ABCDEFGH")
    E = [('A', 'B'), ('A', 'C'), ('A', 'G'), ('A', 'H'),
          ('B', 'C'), ('B', 'F'),
          ('C', 'D'),
          ('D', 'E'),
          ('E', 'F'),
          ('H', 'F')]

    g = Graph(V, E)
    print('\nUndirected Graph')
    print('|V|:', g.num_vertices())
    print('|E|:', g.num_edges())
    print('Adjacent to A:', g['A'])
    print(g.G)


if __name__ == '__main__':
    main()
        