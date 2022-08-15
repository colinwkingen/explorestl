"""
A flat triangular surface representing part of a 3d object.
"""


from math import sqrt


class Facet():

    def __init__(self, vertices):
        assert len(vertices) == 3
        self.vertices = vertices

    def get_area(self):
        a0 = Facet._edge_length(self, self.vertices[0], self.vertices[1])
        b0 = Facet._edge_length(self, self.vertices[1], self.vertices[2])
        c0 = Facet._edge_length(self, self.vertices[2], self.vertices[0])

        # Kahan's area calculation formula is less likely to fail than Heron's for very thin triangles
        # https://www.johndcook.com/blog/2020/02/27/numerical-heron/
        a1 = max(a0, b0, c0)
        c1 = min(a0, b0, c0)
        b1 = (a0 + b0 + c0) - a1 - c1

        inner_terms = (a1+(b1+c1))*(c1-(a1-b1))*(c1+(a1-b1))*(a1+(b1-c1))
        kahan_area = 0.25 * ((inner_terms) ** 0.5)

        return kahan_area

    def _edge_length(self, vx1, vx2):
        # Edge Calculation:
        # https://www.engineeringtoolbox.com/distance-relationship-between-two-points-d_1854.html
        return sqrt((vx2.x-vx1.x)**2+(vx2.y-vx1.y)**2+(vx2.z-vx1.z)**2)
