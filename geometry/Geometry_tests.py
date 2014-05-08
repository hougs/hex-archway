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

    def flat_hex_position_test(self):
        actual_1by1_hexs = VertexPositioner._flat_hex_pos(1, 1, 1)
        print "1x1: " + str([hex.__dict__ for hex in actual_1by1_hexs])
        expected_1by1_hexs = [Hexagon(1, 0, 0)]
        actual_2by2_hexs = VertexPositioner._flat_hex_pos(1, 2, 2)
        print "2x2: " + str([hex.__dict__ for hex in actual_2by2_hexs])

        expected_2by2_hexs = [Hexagon(1, -1, -1),
                              Hexagon(1, 1, -1),
                              Hexagon(1, -1, 1),
                              Hexagon(1, 1, 1)]

    def flat_has_plot_test(self):
        v_pos = VertexPositioner(1, 4, 7)
        print "vertices: " + str([hex.vertices for hex in v_pos
            .flat_hexagons])
        v_pos.plot_vertices()
