import numpy as np


class Hexagon():
    def __init__(self, side_length, center_x, center_y):
        self.vertices = self._make_vertices(side_length, center_x, center_y)

    @staticmethod
    def _make_vertices(side_length, center_x, center_y):
        vertices = np.empty([6, 2])
        for vertex_number in range(0.0, 5.0, 1.0):
            angle = (vertex_number * np.pi)/3
            x_position = side_length * np.sin(angle)
            y_position = side_length * np.cos(angle)
            vertices[[vertex_number, ]] = [x_position + center_x,
                                           y_position + center_y]
        return vertices

class VertexPositioner():
    def __init__(self, approx_hex_side_length, n_hex_x_rows, n_hex_y_rows):
        """
        Our strategy for positioning these hexagons in a cylindrical fashion is
        to first tessealte a rectangle with the specified number of hexagons,
        and then map that rectangle on to the surface of a cylinder in a
        distance preserving way. This is easily done by mapping points
            f(x, y) = (x, R sin(th), R cos(th))
            where th = (pi * y)/(2 * n_hex_y_rows * approx_side_length)
        In order to define the number of hexagons in a row as an integer, we
        will add the constraint that if we formed a toroid out of our
        rectangle, our hexagons would still tesselate it.
        """
        self.flat_hexagons = self._flat_hex_pos(approx_hex_side_length,
                                            n_hex_x_rows,
                                           n_hex_y_rows)
        self.vertex_positions = self._rect_to_cyl()

    @staticmethod
    def _flat_hex_pos(hex_side_length, n_hex_x_row, n_hex_y_row):
        """ Returns a list of Hexagons that comprise the tessalation of a
        rectangle. When we form a cylinder out of this rectangle, the rows of
        hexagons parallel to the x-axis will remain ~flat lines
        and the rows of hexagons parallel to the y-axis will become ~semi
        circles.


        Parameters
        ==========
        hex_side_length -- side length of our hexagonal tile.
        n_hex_x_row -- number of hexagonal tiles in the x direction. These
            account for the desired width of the archway.
        n_hex_y_row -- number of hexagonal tiles in the y direction. These
            account for the desired number of hexagons in the arch.
        """

        seed_pos_x = hex_side_length * (n_hex_x_row - 1)
        seed_pos_y = hex_side_length * (n_hex_y_row - 1)
        hexagons = []
        for center_x in range(-seed_pos_x, seed_pos_x, hex_side_length):
            for center_y in range(-seed_pos_y, seed_pos_y, hex_side_length):
                hexagons.append(Hexagon(hex_side_length, center_x, center_y))
        return hexagons

    def _rect_to_cyl_coords(self, radius, x, y):
        """
        (x, y) -> (x, R sin(th), R cos(th))
        where th = (pi * y)/(2 R)
        """
        theta = (np.pi * y)/(radius * 2)
        x = radius * np.sin(theta)
        y = radius * np.cos(theta)
        return (x, y)



