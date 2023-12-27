import numpy as np
import scipy.sparse as sp
import heapdict

class Graph:
    def __init__(self):
        """ Initialize with an empty edge dictionary. """
        self.edges = {}
        self.nodes = set()
        self.A = False
        self.nlist = []
    
    def add_edges(self, edges_list):
        """ Add a list of edges to the network.
        
        Args:
            edges_list: list of (a,b) tuples, where a->b is an edge to add
        """       
        for left, right in edges_list:
            if left in self.edges:
                 self.edges[left].update({right: 1.0})
            else:
                self.nodes.add(left)
                self.edges[left] = {right: 1.0}
            
            if right not in self.edges:
                self.nodes.add(right)                
                self.edges[right] = {}

    def get_neighbors(self, node):
        neighbors = set(self.edges[node].keys())
        return neighbors
    
    def shortest_path(self, source):
        """ Compute the single-source shorting path.
        
        This function uses Djikstra's algorithm to compute the distance from 
        source to all other nodes in the network.
        
        Args:
            source: node index for the source
            
        Returns: tuple: dist, path
            dist: dictionary of node:distance values for each node in the graph, 
                  where distance denotes the shortest path distance from source
            path: dictionary of node:prev_node values, where prev_node indicates
                  the previous node on the path from source to node
        """
        
        Q = self.nodes.copy()
        dist = {}
        path = {}

        for vertex in Q:
            dist[vertex] = float("inf")
            path[vertex] = None

        # Distance from source to itself
        dist[source] = 0 

        hdist = heapdict.heapdict(dist)                       

        while Q:
            u = hdist.popitem()[0]
            Q.remove(u)
            neighbors = self.get_neighbors(u)
            neighbors = neighbors.intersection(Q)

            for neighbor in neighbors:
                alt = dist[u] + 1
                if alt < dist[neighbor]:
                    dist[neighbor] = alt 
                    hdist[neighbor] = alt 
                    path[neighbor] = u 

        return dist, path

    def adjacency_matrix(self):
        """ Compute an adjacency matrix form of the graph.  
        
        Returns: tuple (A, nodes)
            A: a sparse matrix in COO form that represents the adjacency matrix
               for the graph (i.e., A[j,i] = 1 iff there is an edge i->j)
               NOTE: be sure you have this ordering correct!
            nodes: a list of nodes indicating the node key corresponding to each
                   index of the A matrix
        """
        nodes = list(self.nodes)
        nodeIndexDict = {node: i for i, node in enumerate(nodes)}
        col = np.array([nodeIndexDict[src_key] for src_key, valdict in self.edges.items() for trgt_key in valdict.keys()])
        row = np.array([nodeIndexDict[trgt_key] for src_key, valdict in self.edges.items() for trgt_key in valdict.keys()])

        data = np.ones(len(row), dtype=np.int)
        
        A = sp.coo_matrix((data, (row, col)))
        
        self.A = A
        self.nlist = nodes
        return A, nodes
    
    def pagerank(self, d=0.85, iters=100):
        """ Compute the PageRank score for each node in the network.
        
        Compute PageRank scores using the power method.
        
        Args:
            d: 1 - random restart factor
            iters: maximum number of iterations of power method
            
        Returns: dict ranks
            ranks: a dictionary of node:importance score, for each node in the
                   network (larger score means higher rank)
        
        """
        A, nlist = self.adjacency_matrix()
        sumA = np.array(A.sum(axis=0))[0]
        invSumA = 1.0 / sumA
        xpd_invSumA = np.array([invSumA[col] for col in A.col])
        A.data = A.data * xpd_invSumA * d

        # intialize ranks to uniform dist
        rank = np.array([1.0 / len(nlist)] * len(nlist))

        for i in range(iters):
            rank = A.dot(rank) + (1 - d) * 1.0 / len(nlist)

        rank = rank / sum(rank)
        ranks = dict(zip(nlist, rank))
        return ranks
