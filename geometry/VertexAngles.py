import numpy as np

class VertexAngles():
    def __init__(self, nodes, edges):
        assert isinstance(nodes, np.array)
        assert isinstance(edges, list)
        #
        self.node_to_edge_dict = {node: list() for node in nodes}
        # a list of Edges
        self.edges = edges

    def _fill_node_edge_dict(self):
        #TODO(juliet): how does this compare to vertex
        for edge in self.edges:
            #update edge information for both endpoints (that are also vertices)
            self.node_to_edge_dict[edge.nodes[0]] = self.node_to_edge_dict[edge.nodes[0]].add(edge.nodes[1])
            self.node_to_edge_dict[edge.nodes[1]] = self.node_to_edge_dict[edge.nodes[1]].add(edge.nodes[0])
        return self


def main(self):
    print "Nodes are: {}".format(self.nodes)
    print "Edgeses are: {}".format(self.edges)

if __name__ == "__main__": main()