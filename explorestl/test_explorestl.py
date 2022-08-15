"""
Testing explorestl to ensure files are successfully parsed.
"""

import pytest
from .main import Vertex, Solid, Facet, parse_stl_file


def test_vertex_instantiation_success():
    vtx = Vertex(4, 3, 4)
    assert vtx


def test_vertex_instantiation_fail_on_bad_type():
    with pytest.raises(Exception):
        vtx = Vertex("foo", 3, 4)
        assert vtx


def test_facet_instantiation_success():
    vtx0 = Vertex(4, 2, 4)
    vtx1 = Vertex(4, 3, 6)
    vtx2 = Vertex(1, 3, 4)
    facet = Facet([vtx0, vtx1, vtx2])
    assert facet


def test_facet_instantiation_fail_on_wrong_num_vertices():
    vtx0 = Vertex(4, 2, 4)
    vtx1 = Vertex(4, 3, 6)
    with pytest.raises(Exception):
        facet = Facet([vtx0, vtx1])


def test_facet_get_area():
    vtx0 = Vertex(4, 2, 4)
    vtx1 = Vertex(4, 3, 6)
    vtx2 = Vertex(1, 3, 4)
    facet = Facet([vtx0, vtx1, vtx2])

    assert facet.get_area() == 3.5000000000000013


def test_solid_instantiation_success():
    vtx0 = Vertex(4, 2, 4)
    vtx1 = Vertex(4, 3, 6)
    vtx2 = Vertex(1, 3, 4)
    facet = Facet([vtx0, vtx1, vtx2])
    solid = Solid()
    solid.add_facet(facet)
    assert solid
    assert len(solid.facets) == 1


def test_analyze_moon_stl():
    result = parse_stl_file("stl_files/moon.stl")
    assert result == (116, 7.772634278919951)


def test_analyze_simple_stl():
    result = parse_stl_file("stl_files/simple.stl")
    assert result == (2, 1.4142135623730954)

