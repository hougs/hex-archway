import numpy as np

class VertexAngles():
    def __init__(self, nodes, edges):
        assert isinstance(nodes, np.array)
        assert isinstance(edges, list)
        self.node_to_edge_dict = self._fill_node_edge_dict(edges, nodes)


    @staticmethod
    def _fill_node_edge_dict(edges, nodes):
        node_to_edge = {node: list() for node in nodes}
        for edge in edges:
            origin0, disp0, origin1, disp1 = edge.origins_and_displacements()
            node_to_edge[origin0].append(disp0)
            node_to_edge[origin1].append(disp1)
        return node_to_edge


def main():
    # add things here

if __name__ == "__main__": main()