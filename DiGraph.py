import networkx as nx
from semanticnet import Graph

class DiGraph(Graph):

    def __init__(self, verbose=False):
        super(DiGraph, self).__init__()
        self._g = nx.MultiDiGraph()

    def remove_node(self, id_):
        '''Removes node id_.'''
        id_ = self._extract_uuid(id_)
        if self._g.has_node(id_):
            # for DiGraph, remove predecessors AND successors
            for successor in self._g.neighbors(id_):
                # need to iterate over items() (which copies the dict) because we are
                # removing items from the edges dict as we are iterating over it
                for edge in self._g.edge[id_][successor].items():
                    self.remove_edge(self._g.edge[id_][successor][edge[0]]["id"]) # edge[0] is the edge's ID
            for predecessor in self._g.predecessors(id_):
                for edge in self._g.edge[predecessor][id_].items():
                    self.remove_edge(self._g.edge[predecessor][id_][edge[0]]["id"])

            self._g.remove_node(id_)
        else:
            raise GraphException("Node ID not found.")