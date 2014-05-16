from VertexPositioner import Hexagon
from VertexPositioner import VertexPositioner
import numpy.testing as nptst
import itertools as it

class Geometry_tests():
    def hexagon_test(self):
        hexagon = Hexagon(1, 0, 0)
        nptst.assert_almost_equal(hexagon.vertices[0][0], 0)
        nptst.assert_almost_equal(hexagon.vertices[0][1], 1)
        nptst.assert_almost_equal(hexagon.vertices[3][0], 0)
        nptst.assert_almost_equal(hexagon.vertices[3][1], -1)


    def flat_has_plot_test(self):
        v_pos = VertexPositioner(1, 4, 7)
        print v_pos._vertex_to_neighbor_dict()
        v_pos.plot_vertices()
