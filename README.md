[![N|Python](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

[![CircleCI](https://circleci.com/gh/fusion-energy/cad_to_h5m/tree/main.svg?style=svg)](https://circleci.com/gh/fusion-energy/cad_to_h5m/tree/main) [![CI with docker build](https://github.com/fusion-energy/cad_to_h5m/actions/workflows/ci_with_docker_build.yml/badge.svg)](https://github.com/fusion-energy/cad_to_h5m/actions/workflows/ci_with_docker_build.yml)

[![PyPI](https://img.shields.io/pypi/v/cad-to-h5m?color=brightgreen&label=pypi&logo=grebrightgreenen&logoColor=green)](https://pypi.org/project/cad-to-h5m/)


<!-- can't report coverage as cubit init changes scope
[![codecov](https://codecov.io/gh/fusion-energy/cad_to_h5m/branch/main/graph/badge.svg)](https://codecov.io/gh/fusion-energy/cad_to_h5m) -->

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
separate material tags for each STP file and saves the result as a h5m file.

```bash
cad-to-h5m -i part1.stp part2.stp -o dagmc.h5m -t mat:1 mat:2 -c /opt/Coreform-Cubit-2021.5/bin/
```

It is also possible to convert .sat files in the following way.

```bash
cad-to-h5m -i part1.sat -o dagmc.h5m -t mat:1 -c /opt/Coreform-Cubit-2021.5/bin/
``` -->

# Installation

The package is available via the PyPi package manager and the recommended
method of installing is via pip.
```bash
pip install cad_to_h5m
```

In addition [Cubit](https://coreform.com/products/coreform-cubit/) and the 
[Svalinn Plugin](https://github.com/svalinn/Cubit-plugin) needs to be
installed to make full use of this package.

# Python API usage

Creating a h5m file from a single STP file called ```part1.stp``` and applying
a material tag to the volume.

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags=[{'cad_filename':'part1.stp', 'material_tag':'m1'}],
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
    files_with_tags=[
        {'cad_filename':'part1.stp', 'material_tag':'m1'},
        {'cad_filename':'part2.stp', 'material_tag':'m2'}
    ],
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
)
```

Creating a h5m file from a single SAT is a similar process. Note the .sat file
extension.

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags=[{'cad_filename':'part1.sat', 'material_tag':'m1'}],
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
)
```

Creating a tet mesh files compatible with the OpenMC / DAGMC Unstructured mesh
format is also possible. Another key called ```tet_mesh``` to the ```files_with_tags``` dictionary will trigger the meshing of that CAD file.
The value of the key will be passed to the Cubit mesh command as an instruction.
The following command will produce a ```unstructured_mesh_file.exo```
file that can then be used in DAGMC compatible neutronics codes. There are examples
[1](https://docs.openmc.org/en/latest/examples/unstructured-mesh-part-i.html)
[2](https://docs.openmc.org/en/latest/examples/unstructured-mesh-part-ii.html) 
for the use of unstructured meshes in OpenMC.

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags=[
        {
            'cad_filename':'part1.sat',
            'material_tag':'m1',
            'tet_mesh': 'size 0.5'
        }
    ],
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
    exo_filename='unstructured_mesh_file.exo'
)
```

Use if ```exo``` files requires OpenMC to be compiled with LibMesh. OpenMC also
accepts DAGMC tet meshes made with MOAB which is another option. The following
example creates a ```cub``` file that contains a mesh. The MOAB tool 
```mbconvert``` is then used to extract the tet mesh and save it as a ```h5m```
file which cna be used in OpenMC as shown in the OpenMC [examples](https://docs.openmc.org/en/stable/examples/unstructured-mesh-part-i.html)

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags=[
        {
            'cad_filename':'part1.sat',
            'material_tag':'m1',
            'tet_mesh': 'size 0.5'
        }
    ],
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
    cubit_filename='unstructured_mesh_file.cub'
)
```
The ```cub``` file produced contains a tet mesh as well as the faceted geometry.
The tet mesh can be extracted and converted to another ```h5m``` file for use in
OpenMC. MOAB is needed to convert the file and includes the command line tool
```mbconvert```, MOAB can be installed into a Conda environment with:

```
conda install -c conda-forge moab
```
Then ```mbconvert``` can be used to extract and convert the tet mesh from the
```cub``` file into a ```h5m``` file.

```bash
mbconvert unstructured_mesh_file.cub unstructured_mesh_file.h5m
```

Scaling geometry is also possible. This is useful as particle transport codes
often make use of cm as the default unit. CAD files typically appear in mm as
the default limit. Some CAD packages ignore units while others make use of them.
The h5m files are assumed to be in cm by particle transport codes so often it
is necessary to scale up or down the geometry. This can be done by adding
another key called ```scale``` and a value to the ```files_with_tags```
dictionary. This example multiplies the geometry by 10.

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags=[
        {
            'cad_filename':'part1.sat',
            'material_tag':'m1',
            'scale': 10
        }
    ],
    h5m_filename='dagmc.h5m',
)
```

Assigning a material to the implicit complement is also possible. This can be useful on large complex geometries where boolean operations can result in robustness issues. This is implemented by assigning the desired material tag of the implicit complement to the optional ```implicit_complement_material_tag``` argument. Defaults to vacuum.

```python
from cad_to_h5m import cad_to_h5m

cad_to_h5m(
    files_with_tags=[
        {
            'cad_filename':'part1.sat',
            'material_tag':'m1',
        }
    ],
    h5m_filename='dagmc.h5m',
    implicit_complement_material_tag = 'm2'
)
```
