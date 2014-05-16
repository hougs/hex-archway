import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
            x_position = side_length * np.cos(angle)
            y_position = side_length * np.sin(angle)
            vertices[vertex_number, :] = np.array([x_position + center_x,
                                                   y_position + center_y])
        return vertices

class Edge():
    def __init__(self, nodes):
        assert len(nodes) == 2
        self.nodes = nodes

    def get_vector(self):
        return self.nodes[0] - self.nodes[1]


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
        self.n_hex_x_rows = n_hex_x_rows
        self.n_hex_y_rows = n_hex_y_rows
        self.arch_radius = n_hex_y_rows * approx_hex_side_length
        self.flat_hexagons = self._flat_hex_pos(approx_hex_side_length)
        # a n_hex_x_rows by n_hex_y_rows by 6 by 3 np.array
        self.arch_vertex_positions = self._position_uniq_vertices()
        self.edges = self._id_edges()

    def _flat_hex_pos(self, hex_side_length):
        """ Returns a list of Hexagons that comprise the tessalation of a
        rectangle. When we form a cylinder out of this rectangle, the rows of
        hexagons parallel to the x-axis will remain ~flat lines
        and the rows of hexagons parallel to the y-axis will become ~semi
        circles.

        *   *   *
          *   *
        *   *   *


        Parameters
        ==========
        hex_side_length -- side length of our hexagonal tile.
        n_hex_x_row -- number of hexagonal tiles in the x direction. These
            account for the desired width of the archway.
        n_hex_y_row -- number of hexagonal tiles in the y direction. These
            account for the desired number of hexagons in the arch.
        """
        x_row_displacement = 3 * hex_side_length
        y_row_displacement = 2 * hex_side_length * np.cos(np.pi / 6.0)
        hexagons = np.empty(shape=[self.n_hex_x_rows, self.n_hex_y_rows], dtype=np.dtype(object))
        for x_hex_idx in range(0, self.n_hex_x_rows, 1):
            for y_hex_idx in range(0, self.n_hex_y_rows, 1):
                center_x = x_row_displacement * x_hex_idx
                center_y = y_hex_idx * y_row_displacement
                hexagons[x_hex_idx, y_hex_idx] = Hexagon(hex_side_length, center_x, center_y)
        return hexagons

    def _id_edges(self):
        edge_list = []
        # identify all edges along the hexagons we explicitly index
        for x_hex_idx in range(0, self.n_hex_x_rows, 1):
            for y_hex_idx in range(0, self.n_hex_y_rows, 1):
                for vertex_idx in range(0, 6, 1):
                    first_end_pt = self.arch_vertex_positions[x_hex_idx, y_hex_idx, vertex_idx, :]
                    if vertex_idx == 5:
                        second_end_pt = self.arch_vertex_positions[x_hex_idx, y_hex_idx, 0, :]
                    else:
                        second_end_pt = self.arch_vertex_positions[x_hex_idx, y_hex_idx, vertex_idx + 1, :]
                    edge_list.append(Edge(np.array([first_end_pt, second_end_pt])))

        # identify edges that help form the implicit hexagon in between the explicitly indexed hexagons
        for x_hex_idx in range(0, self.n_hex_x_rows - 1, 1):
            for y_hex_idx in range(0, self.n_hex_y_rows, 1):
                first_end_pt = self.arch_vertex_positions[x_hex_idx, y_hex_idx, 0, : ]
                second_end_pt = self.arch_vertex_positions[x_hex_idx + 1, y_hex_idx, 3, :]
                edge_list.append(Edge(np.array([first_end_pt, second_end_pt])))
        return edge_list

    def _rect_to_cyl_coords(self, x, y):
        """
        (x, y) -> (x, R sin(th), R cos(th))
        where th = (pi * y)/(2 R)
        """
        theta = (np.pi * y) / (self.arch_radius * 2)
        y = self.arch_radius * np.sin(theta)
        z = self.arch_radius * np.cos(theta)
        return np.array([x, y, z])

    def _position_uniq_vertices(self):
        """
        Returns a n_hex_x_rows by n_hex_y_rows by 6 by 3 np.array. The first two indices of this array locate which
        hexagon in the tiling the vertex originated from. The 3rd index represent where on the hexagon the vertex is
        located. If we measure the angle th such that th=0 is in the positive x direction, the following correspondences
        hold:
            hex_3d_vertices[:, :, 0, :] ~ vertices where th = 0
            hex_3d_vertices[:, :, 1, :] ~ vertices where th = pi/3
            hex_3d_vertices[:, :, 2, :] ~ vertices where th = 2 pi/3
            hex_3d_vertices[:, :, 3, :] ~ vertices where th = pi
            hex_3d_vertices[:, :, 4, :] ~ vertices where th = 4 pi/3
            hex_3d_vertices[:, :, 5, :] ~ vertices where th = 5 pi/3
        Parameters:
        hexagons -- a list of Hexagons.
        Returns a list of unique (x, y, z) coordinates representing vertices of
        our surface as 3-tuples.
        """
        hex_3d_vertices = np.empty(shape=[self.n_hex_x_rows, self.n_hex_y_rows, 6, 3])
        for x_hex_idx in range(0, self.n_hex_x_rows, 1):
            for y_hex_idx in range(0, self.n_hex_y_rows, 1):
                for vertex_index in range(0, 6, 1):
                    vertices = self.flat_hexagons[x_hex_idx, y_hex_idx].vertices
                    hex_3d_vertices[x_hex_idx, y_hex_idx, vertex_index, :] = \
                        self._rect_to_cyl_coords(vertices[vertex_index, 0], vertices[vertex_index, 1])
        return hex_3d_vertices

    def plot_vertices(self):
        fig = plt.figure()
        ax = fig.add_subplot(131)
        for x_hex_idx in range(0, self.n_hex_x_rows, 1):
            for y_hex_idx in range(0, self.n_hex_y_rows, 1):
                hexagon = self.flat_hexagons[x_hex_idx, y_hex_idx]
                ax.scatter(hexagon.vertices[:, 0], hexagon.vertices[:, 1])

        plt.title("flat hexagons")
        ax.axis('equal')
        ax2 = fig.add_subplot(132, projection='3d')
        for x_hex_idx in range(0, self.n_hex_x_rows, 1):
            for y_hex_idx in range(0, self.n_hex_y_rows, 1):
                vertices = self.arch_vertex_positions[x_hex_idx, y_hex_idx, :, :]
                ax2.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2])
        ax3 = fig.add_subplot(133, projection='3d')
        for edge in self.edges:
            ax3.plot(edge.nodes[:, 0], edge.nodes[:, 1], edge.nodes[:, 2])
        plt.show()

