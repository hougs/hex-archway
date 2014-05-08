import numpy as np
import matplotlib.pyplot as plt


class Hexagon():
    def __init__(self, side_length, center_x, center_y):
        self.center_x = center_x
        self.center_y = center_y
        self.vertices = self._make_vertices(side_length, center_x, center_y)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    @staticmethod
    def _make_vertices(side_length, center_x, center_y):
        vertices = np.empty(shape=[6, 2])

        for vertex_number in range(0, 6, 1):
            angle = (vertex_number * np.pi) / 3
            x_position = side_length * np.sin(angle)
            y_position = side_length * np.cos(angle)
            vertices[vertex_number, :] = np.array([x_position, y_position])
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
        self.arch_radius = n_hex_y_rows * approx_hex_side_length
        self.flat_hexagons = self._flat_hex_pos(approx_hex_side_length,
                                                n_hex_x_rows,
                                                n_hex_y_rows)
        self.arch_vertex_positions = self._position_uniq_vertices()

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

        seed_pos_x = hex_side_length * (n_hex_x_row)
        seed_pos_y = hex_side_length * (n_hex_y_row)
        hexagons = []
        for center_x in range(-seed_pos_x, seed_pos_x, 2 * hex_side_length):
            for center_y in range(-seed_pos_y, seed_pos_y,
                                  2 * hex_side_length):
                hexagons.append(Hexagon(hex_side_length, center_x, center_y))
        return hexagons

    def _rect_to_cyl_coords(self, xy_array):
        """
        (x, y) -> (x, R sin(th), R cos(th))
        where th = (pi * y)/(2 R)
        """
        x = xy_array[0]
        y = xy_array[1]
        theta = (np.pi * y) / (self.arch_radius * 2)
        y = self.arch_radius * np.sin(theta)
        z = self.arch_radius * np.cos(theta)
        return (x, y, z)

    def _position_uniq_vertices(self):
        """
        Parameters
        ==========
        hexagons -- a list of Hexagons.
        Returns a list of unique (x, y, z) coordinates representing vertices of
        our surface as 3-tuples.
        """
        coords_3d = []
        for hexagon in self.flat_hexagons:
            coords_3d.append(np.apply_along_axis(self._rect_to_cyl_coords,
                                                 axis=1, arr=hexagon
                                                 .vertices))
        return coords_3d

    def plot_vertices(self):
        plt.subplot(1, 1, 1)

        x_pos = np.empty(shape=[len(self.flat_hexagons) * 6, 1])
        y_pos = np.empty(shape=[len(self.flat_hexagons) * 6, 1])
        for hex, idx in zip(self.flat_hexagons, range(0, len(self
                .flat_hexagons), 1)):
            x_pos[(idx * 6):((idx + 1) * 6), 0] = hex.vertices[:, 0]
            y_pos[(idx * 6):((idx + 1) * 6), 0] = hex.vertices[:, 1]
        plt.scatter(x_pos, y_pos)
        plt.title("flat hexagons")
        plt.show()






