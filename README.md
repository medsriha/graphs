# Graphs
Implementation  Djisktra's algorithm for finding single-source shortest paths in the graph, and the PageRank algorithm for determining the importance of nodes in the network.

### The test graph
The graph we'll be focusing on is a directed graph that represents the page links in the English language Wikipedia. Specifically, we took the (pre-processed) Wikipedia dump from here: http://haselgrove.id.au/wikipedia.htm , which were taken from a 2008 version of Wikipedia, and we then selected only subselected only those nodes that had at least 500 incoming links. This resulted in a graph with about 24 thousands that had about 6 million edges between the nodes.

Our own Graph class
In the main portion, we'll create our own Graph class that mimics some of the functionality of networkx (and which will indeed be much faster than networkx when it comes to algorithms like PageRank).
