"""
A 3D representation of an object as a collection of triangular facets.
"""


class Solid():
    facets = []
    area = 0.0

    def add_facet(self, facet):
        self.facets.append(facet)
        self.area = facet.get_area() + self.area

    def clear(self):
        """
        Mostly for the benefit of Pytest as it likes to hold the solid in
        memory when it tests multiple STL files.
        """
        self.facets.clear()
        self.area = 0.0

