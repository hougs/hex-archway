import numpy as np

class VertexAngles():
    def __init__(self, nodes, edges):
        assert isinstance(nodes, np.array)
        assert isinstance(edges, list)
        self.nodes = nodes
        self.edges = edges

