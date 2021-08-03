
import cad_to_h5m as c2h
import urllib.request

url = 'https://raw.githubusercontent.com/Shimwell/fusion_example_for_openmc_using_paramak/main/stp_files/blanket.stp'
urllib.request.urlretrieve(url, 'blanket.stp')

c2h.stp_converter(
    # input={'part1.stp':'mat1'},
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
)
