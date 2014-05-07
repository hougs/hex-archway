from VertexPositioner import Hexagon
import numpy.testing as nptst

class Geometry_tests():
    def hexagon_test(self):
        hexagon = Hexagon(1, 0, 0)
        print "vertices: " + str(hexagon.vertices)
        nptst.assert_almost_equal(hexagon.vertices[0, 0], 0)
        nptst.assert_almost_equal(hexagon.vertices[0, 1], 1)
        nptst.assert_almost_equal(hexagon.vertices[3, 0], 0)
        nptst.assert_almost_equal(hexagon.vertices[3, 1], -1)
