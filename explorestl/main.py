"""

The purpose of this Python program is to get a count of triangles and a measure of surface area from a ASCII STL file.
In order to do this we will:

1. Load the file
2. Iterate through the triangles within it by looking for keywords.
3. Accumulate three vertices for each triangle.
4. Calculate the area of each triangle and add to a running total.
5. Return a count of triangles, and the aggregated area.

"""

from pathlib import Path
from solid import Solid
from vertex import Vertex
from facet import Facet
import constant as constant


def parse_stl_file(file_path_text=None):
    if not file_path_text:
        file_path_text = constant.DEFAULT_FILE_PATH
    file_path = Path(file_path_text)
    if not file_path.is_file():
        print(constant.INVALID_FILE)
    else:
        with open(file_path) as stl_file:
            if stl_file and next(stl_file).strip().startswith(constant.SOLID):
                solid = Solid()
                solid.clear()
                vtx_buffer = []
                for line in stl_file:
                    line = line.strip()
                    if line.startswith(constant.VERTEX):
                        vtx = line.split(" ")
                        vtx_buffer.append(Vertex(x=vtx[1], y=vtx[2], z=vtx[3]))
                    elif line.startswith(constant.ENDLOOP):
                        new_facet = Facet(vtx_buffer.copy())
                        vtx_buffer.clear()
                        solid.add_facet(new_facet)
                stl_file.close()
                resp = len(solid.facets), solid.area
                return resp


def gather_input():
    print(constant.ASK_FOR_INPUT)
    filename = input(">>")
    resp = parse_stl_file(filename)
    print(f"Number of Triangles --> {str(resp[0])}")
    print(f"Surface Area        --> {str(resp[1])}")


if __name__ == '__main__':
    gather_input()
