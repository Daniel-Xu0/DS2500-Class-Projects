"""
Daniel Xu
November 7th, 2021
Homework #4 - Weighted Graphing
Professor Park
"""
from graph import Graph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

GENES = 'gad_data.csv'

#%% Weighted Graph Class
class WeightedGraph(Graph):
    
    kind = 'graph'
    
    def __init__(self, V = [], E = []):
        """ Constructor: inherits from parent graph class """
        super().__init__(V, E)
    
    def add_edge(self, u, v):
        """ Have to change add_edge method since after adding a weight param,
            edges now have a tuple inside of a tuple """
            
        # add vertices in case they don't already exist
        weighted_edge = list(v)
        self.add_vertex(u)
        self.add_vertex(weighted_edge[0])

        # add undirected edge (u,v)
        self.G[u].add(v)
        self.G[weighted_edge[0]].add((u, weighted_edge[1]))
    
    def subgraph(self, nodes, exclusive = True):
        """ 
        Method: Create a subgraph from the original graph with only the 
                  specified nodes 
        Parameters: list of nodes, exclusivity parameter: True causes 
                    the method to check that both the vertices and edges are
                    in the specified nodes list param.
                    False creates an adjacency list where the vertices are in
                    the nodes list param, but the edges don't have to be.
        Return: An adjacency list with just the nodes specified
        """
        # Create an empty subgraph dictionary
        subgraph = {}
        
        # If vertices and adjacent vertices both have to be in nodes list, 
        # continue down this path
        if exclusive:
            for node in nodes:
                subgraph[node] = set()
                for edge in self.G[node]:
                    if edge[0] in nodes:
                        subgraph[node].add(edge)
        
        # If just the vertices have to be in the nodes list, continue
        # down this path
        else:
            for node in self.G:
                if node in nodes:
                    subgraph[node] = self.G[node]
                    
        subgraph_str = ''
        for v in subgraph:
            subgraph_str += '['+v+'] => ' + str(subgraph[v]) + '\n'
            
        print("Here's your subgraph: \n", subgraph_str)
        return subgraph

    def degree_distribution(self, title):
        """
        Method: Plot the degree distribution of all vertices within the 
                adjacency list
        Parameters: None
        Return: A lineplot illustrating the number of vertices with a certain
                degree
        """
        # Count the number of adjacent vertices each node has
        edge_lst = [len(value) for value in self.G.values()]
        
        # Find the greatest amount of vertices one node has
        max_degree = max(edge_lst)
        
        # Create and add to degree bins
        degree_bins = [0] * max_degree
        
        for v in self.G:

            degree_bins[self.deg(v)-1] += 1
        
        # Plot the bins as a scatterplot
        fig, ax = plt.subplots()
        ax.loglog([i+1 for i in range(len(degree_bins))], degree_bins, 'o',
                    color = np.random.rand(3,))
        
        ax.set(title = title, xlabel = 'Degree', ylabel = 'Number of Vertices')
        plt.savefig('Degree Distribution')
        plt.show()
        
    def plot_graph(self, subgraph):
        '''
        Method: Generate visualization of network
        Parameters: Adjacency list (dictionary)
        Return: A network graph of the adjacency list
        '''
        # Create an instance of the networkx graph class
        G = nx.DiGraph()
        # Add in my edges
        edge_labels = {}
        for key, value in subgraph.items():
            for edge, weight in value:
                edge_labels[(key, edge)] = weight
                G.add_edge(key, edge)
        
        # Create the actual network figure
        plt.figure(3,figsize=(15,15)) 
        
        pos = nx.spring_layout(G)
        nx.draw_networkx(G, pos, node_color = 'pink', width = 1, linewidths = 1,
                         with_labels = True)
        
        nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels)
        
        # Set margins for the axes so that nodes aren't clipped
        ax = plt.gca()
        ax.margins(.00001)
        plt.axis("off")
        plt.savefig('Asthma Related Genes and Diseases Network')
        plt.show()
        

#%% CSV to weighted graph method

def csv_to_wgraph(filename, vertex_col, edge_col, weight_col):
    '''
    Function: Reads in a csvfile and cleans it up
    Parameters: filename (str), list of columns you want to delete
    Return: csvfile data as a graph
    '''      
    # Turn file into a dataframe
    df = pd.read_csv(filename)
    
    # Turn inputted column into a list of vertices
    vertices = list(df[vertex_col])
    
    # Zip edge_col and weight_col together
    edges = zip(list(df[edge_col]), list(df[weight_col]))
    
    # Zip the vertices and edges together to make an edge list
    edge_lst = zip(vertices, edges)  

    # Turn the adjacency list into a weighted graph
    graph = WeightedGraph(vertices, edge_lst)
    
    return graph

#%% Main 

if __name__ == "__main__":
    
    # Example list of vertices and edges to turn into a weighted graph object
    V = list("ABCDE")
    E = [('A', ('B', 5)), ('A', ('C', 3)), ('A', ('D', 10)),
          ('B', ('A', 5)), ('B', ('D', 4)),
          ('C', ('A', 3)),
          ('D', ('A', 10)), ('D', ('B', 4)), ('D', ('E', 7)),
          ('E', ('D', 7))]
          
    graph = WeightedGraph(V, E)

    # Turn the gad_data_csv file into a weighted graph object
    gene_to_disease = csv_to_wgraph(GENES, 'gene', 'disease', 'num_positive')
    
    # Plot the degree distribution of the gene-disease graph
    gene_to_disease.degree_distribution('Number of related Diseases to a Gene')
    
    '''
    It seems that the gene-disease association network isn't that scale free. 
    Of course, there are a ton of genes/vertices that only have one adjacent 
    vertex, but there are also quite a lot that have many connections, hence the 
    quite large cluster of points in the bottom right.
    '''
    
    # Find the genes that are related to asthma and find the diseases 
    # related to each of those genes
    asthma_genes = list(gene_to_disease['asthma'])
    asthma_rel_disease = [gene_to_disease[gene[0]] for gene in asthma_genes]
    
    # Plot the asthma-related genes and each of their respective related 
    # diseases as a subgraph
    asthma_subgraph = gene_to_disease.subgraph([gene[0] for gene in asthma_genes],
                                                exclusive = False)
    
    gene_to_disease.plot_graph(asthma_subgraph)
    '''
    It's a little hard to tell, but I believe that the strongly related diseases 
    to Asthma are Type 1 Diabetes and Graves Disease, among others that I can't
    see.
    '''

    