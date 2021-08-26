[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CircleCI](https://circleci.com/gh/fusion-energy/cad_to_h5m/tree/main.svg?style=svg)](https://circleci.com/gh/fusion-energy/cad_to_h5m/tree/main) [![CI with docker build](https://github.com/fusion-energy/cad_to_h5m/actions/workflows/ci_with_docker_build.yml/badge.svg)](https://github.com/fusion-energy/cad_to_h5m/actions/workflows/ci_with_docker_build.yml)

[![PyPI](https://img.shields.io/pypi/v/cad-to-h5m?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/cad-to-h5m/)

[![codecov](https://codecov.io/gh/fusion-energy/cad_to_h5m/branch/main/graph/badge.svg)](https://codecov.io/gh/fusion-energy/cad_to_h5m)

[![docker-publish-release](https://github.com/fusion-energy/cad_to_h5m/actions/workflows/docker_publish.yml/badge.svg)](https://github.com/fusion-energy/cad_to_h5m/actions/workflows/docker_publish.yml)

This is a minimal Python package that provides both **command line** and
**API** interfaces for converting **multiple** CAD files (STP and SAT format)
into a DAGMC h5m file using the Cubit Python API.

This is useful for creating the DAGMC geometry for use in compatible neutronics
codes such as OpenMC, FLUKA and MCNP.

The geometry is tagged wih material names, optional imprinted and merging
during the process which can speed up particle transport.

<!-- 
# Command line usage

Perhaps the most common use of this program is to convert a STP file into
DAGMC geometry.
```bash
cad-to-h5m -i part1.stp -o dagmc.h5m -t mat:1 -c /opt/Coreform-Cubit-2021.5/bin/
```

- the ```-i``` or ```--input``` argument specifies the input CAD filename(s)
- the ```-o``` or ```--output``` argument specifies the output h5m filename
- the ```-t``` or ```--tags``` argument specifies the tags to apply to the CAD volumes.
- the ```-c``` or ```--cubit``` argument specifies the path to the Cubit python3 folder
- the ```-v``` or ```--verbose``` argument enables (true) or disables (false) the printing of additional details

Multiple STP or SAT files can also be combined and converted into a DAGMC
geometry. This example combines two STP files into a single geometry with
seperate material tags for each STP file and saves the result as a h5m file.

```bash
cad-to-h5m -i part1.stp part2.stp -o dagmc.h5m -t mat:1 mat:2 -c /opt/Coreform-Cubit-2021.5/bin/
```

It is also possible to convert .sat files in the following way.

```bash
cad-to-h5m -i part1.sat -o dagmc.h5m -t mat:1 -c /opt/Coreform-Cubit-2021.5/bin/
``` -->

# Python API usage

Creating a h5m file from a single STP file called ```part1.stp``` and applying
a material tag to the volume.

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags={'filename':'part1.stp', 'material_tags':'m1'},
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
)
```

Creating a h5m file from two STP files called ```part1.stp``` and ```part2.stp```.
Both parts have distinct material tag applied to them and the result is output
as a h5m file with the filename dagmc.h5m.

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags={
        'filename':'part1.stp', 'material_tags':'m1'
        'filename':'part2.stp', 'material_tags':'m2'
    },
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
)
```

Creating a h5m file from a single SAT is a similar process. Note the .sat file
extension.

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags={'filename':'part1.sat', 'material_tags':'m1'},
    h5m_filename='dagmc.h5m',
    tags='mat:1',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
)
```

Creating a EXODUS mesh files compatible with the DAGMC Unstructured  mesh format
is also possible. Another entry must be added to the ```files_with_tags```
argument. The following command will produce a ```unstructured_mesh_file.exo```
file that can then be used in DAGMC compatable neutronics codes. There are examples
[1](https://docs.openmc.org/en/latest/examples/unstructured-mesh-part-i.html)
[2](https://docs.openmc.org/en/latest/examples/unstructured-mesh-part-ii.html) 
for the use of unstructured meshes in OpenMC.

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags={'filename':'part1.sat', 'material_tags':'m1', 'tet_mesh': 'size 0.5'},
    h5m_filename='dagmc.h5m',
    tags='mat:1',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
    exo_filename='unstructured_mesh_file.exo'
)
```

# Installation

The package is available via the PyPi package manager and the recommended
method of installing is via pip.
```bash
pip install cad_to_h5m
```

Some Python dependencies (such as Numpy) are installed during the ```pip install cad_to_h5m``` process, however [Cubit](https://coreform.com/products/coreform-cubit/) needs
to be installed seperatly to make full use of this package.
