
# Explore STL

This is a simple Python 3 program to inspect the number of triangles in an ASCII STL file, and to total their area.

## Installation

This program was written using Python 3.8.10 and Pytest 7.1.2 on a system running Ubuntu 20.04.04. 
Other than pytest, it requires nothing outside the core Python installation.
It should work on any Unix-like operating system including macOS, but is untested and unsupported on Windows.

To run ensure you have Python 3 installed, or install using these instructions:
[https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python]

To install the Pytest dependency, ensure you have pip installed for Python 3 or install like this:

```
$ sudo apt update
$ sudo apt install python3-pip
```

Use pip to install Pytest through a requirements.txt file:

```
$ pip install -r requirements.txt
```

For both pip and and Python, your machine may require you to specify **python3** or **pip3** on the 
command line if you have a default Python 2 installation.

Alternately, you can use a virtual environment to install the requirements if you already have Python >3.4 installed:
[https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment]

If you have activated a virtual environment, install the **requirements.txt** as shown above.

## Testing

Let pytest know where the relevant package resides:
```
$ export PYTHONPATH=explorestl/ pytest
```

Then run the tests:

```
$ pytest
```

## Usage

From the project root directory, run with:

```
$ python3 explorestl/main.py
```

You will be prompted to select an STL file to analyze. A different path should be accepted, but it's easy to 
add files for inspection to the `/stl_files` folder in the project.

Select one:

```
$ stl_files/moon.stl
```

And view the output:

```
Number of Triangles --> 116
Surface Area        --> 7.772634278919951
```

## Design Choices

There are three primary elements we are inspecting in the STL file, represented as classes.
These could have been lists or some other variable representation in a fully function based approach, but I found this to be most readable. It also clearly separates the 3D space concepts
and will allow easy extension of the program.

#### Solid

The entirety of the 3D object. It is represented by a python class that
has two attributes, a list of Facets (triangles) and a running tally of the
solid's area that accumulates as the STL is parsed. Since we accumulate the 
area every time we realize a facet, we don't have to operate on the facets
after creation.

#### Facet

The facet is a triangle comprised of three x,y,z vertices. It is represented by 
a class containing a list of vertices, which it gets on it's initialization.
It holds a method to return the area of the triangle it represents.

The `get_area` function utilizes **Kahan's Area Formula**. There are a few choices
out there, but this one is described as being more tolerant to very thin triangles,
which may occur in 3D objects.

#### Vertex

The vertex is a set of x,y,z coordinates representing a point in 3D space that is a
corner on a triangle. It is instantiated with these coordinates, and does a type check
to ensure that they are valid floats.

#### main.py

This file contains two functions. 

The function `gather_input` will ask the user to specify an STL filename
to process and provide a little guidance. It's simple, but divides the execution of the program into preprocessing and processing.

The function `process_stl_file` extracts data from the STL file to create instances of our classes. It checks for the expected `solid` declaration at the top, then creates `Vertex` instances for each vertex line. When it reaches an `endloop` phrase, it takes the previous three vertices and attempts to make a Facet. It was written to touch each line in the file as little as possible. Checking the vertex buffer size, line keys and using index to find axis values allows it to fail quickly on a malformed file and not output incorrect information.

## Improvements

### Structural

  We could create a class `STLFile` and add functions to validate the file prior to processing and do more sanity checks on the data being extracted.

  The program could more explicitly tell the user what went wrong if a file is not processed, but for this exercise we are assuming well formed ASCII STL files.

  I'd prefer more exception handling for anything accepting outside data like this.

### Performance

  We could probably do better than filling and clearing a `Vertex`
  buffer in `parse_stl_file`. Assigning Vertex one at a time to a Facet and moving to the next one when it was complete could save a little time.

  More area calculation methods could be evaluated for speed. It's possible a faster way exists than Kahan's.

  In large files, we could save area processing to the end and split the list of facets into pieces
  to be processed concurrently. 

  A very large file could itself be split into chunks which could be processed concurrently then accumulated at the end. You could either lightly iterate through the file and split it at
  regular counts of the `facet` keyword, or use a more roughshod approach and split it at a set 
  amount of bytes then use a final function to bring the "jagged edges" together and process them. This split could be done in memory or on the filesystem depending on hardware, and requirements for restarting jobs and and concerns about lost progress.
