import numpy as np

class VertexAngles():
    def __init__(self, nodes, edges):
        assert isinstance(nodes, np.array)
        assert isinstance(edges, list)
        #
        self.node_to_edge_dict = {node: list() for node in nodes}
        # a list of Edges
        self.edges = edges

    @staticmethod
    def _fill_node_edge_dict(edge_list):
        vert_neighbor = []
        #TODO(juliet): can we iter over this list and/or use flat map to make the dict correctly?

        for edge in edge_list:
            node1 = tuple(edge.nodes[0, :])
            node2 = tuple(edge.nodes[1, :])
            vert_neighbor.append([(node1, node2), (node2, node1)])
        return self

    def _vertex_to_neighbor_dict(self):

        vert_neighbor_dict = {}
        for center_edge, edges in groupby(vert_neighbor, itemgetter(0)):
            vert_neighbor_dict[center_edge[0]] = set([])
            for edge in edges:
                assert edge[0][0] == center_edge[0]
                print len(edge)
                print edge[0]
                print edge[1]
                vert_neighbor_dict[edge[0][0]] = \
                    vert_neighbor_dict[edge[0][0]].add(edge[0][1])
        return vert_neighbor_dict


def main(self):
    print "Nodes are: {}".format(self.nodes)
    print "Edgeses are: {}".format(self.edges)

if __name__ == "__main__": main()