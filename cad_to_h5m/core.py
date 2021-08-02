import sys

def stp_converter(
    input='part1.stp',
    output='dagmc.h5m',
    tags='mat:1',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
):

    sys.path.append(cubit_path)
    import cubit
    cubit.init([])
