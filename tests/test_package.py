
import os
import urllib.request
from pathlib import Path

from cad_to_h5m import stp_converter


def test_h5m_creation():
    """Checks that a h5m file is created from stp files"""

    os.system('rm *.h5m')

    url = 'https://raw.githubusercontent.com/Shimwell/fusion_example_for_openmc_using_paramak/main/stp_files/blanket.stp'
    urllib.request.urlretrieve(url, 'blanket.stp')

    stp_converter(
        input='part1.stp',
        output='dagmc.h5m',
        tags='mat:1',
        cubit_path='/opt/Coreform-Cubit-2021.5/bin/python3/'
    )

    assert  Path('dagmc.h5m').is_file()
