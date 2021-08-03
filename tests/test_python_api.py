
import os
import tarfile
import unittest
import urllib.request
from pathlib import Path

import pytest
from cad_to_h5m import cad_to_h5m


class TestExtrudeCircleShape(unittest.TestCase):

    def setUp(self):
        url = 'https://github.com/Shimwell/fusion_example_for_openmc_using_paramak/archive/refs/tags/v0.0.1.tar.gz'
        urllib.request.urlretrieve(url, 'v0.0.1.tar.gz')

        tar = tarfile.open('v0.0.1.tar.gz', "r:gz")
        tar.extractall()
        tar.close()


    def test_h5m_file_creation(self):
        """Checks that a h5m file is created from stp files"""

        os.system('rm dagmc.h5m')

        cad_to_h5m(
            files_with_tags=[
                {
                    'filename':'fusion_example_for_openmc_using_paramak-0.0.1/stp_files/blanket.stp',
                    'material_tag': 'mat1'
                }
            ],
            h5m_filename='dagmc.h5m',
            # cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
            # surface_reflectivity_name='reflective',
            # merge_tolerance=1e-4,
            # cubit_filename='dagmc.cub',
            # geometry_details_filename='geometry_details.json',
            # faceting_tolerance=1.0e-2,
            make_watertight=False,
        )

        assert Path('dagmc.h5m').is_file()

    def test_watertight_h5m_file_creation(self):
        """Checks that a h5m file is created from stp files"""

        os.system('rm dagmc.h5m')

        cad_to_h5m(
            files_with_tags=[
                {
                    'filename':'fusion_example_for_openmc_using_paramak-0.0.1/stp_files/blanket.stp',
                    'material_tag': 'mat1'
                }
            ],
            h5m_filename='dagmc.h5m',
            # cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
            # surface_reflectivity_name='reflective',
            # merge_tolerance=1e-4,
            # cubit_filename='dagmc.cub',
            # geometry_details_filename='geometry_details.json',
            # faceting_tolerance=1.0e-2,
            make_watertight=True,
        )

        assert Path('dagmc.h5m').is_file()

    def test_cub_file_creation(self):
        """Checks that a h5m file is created from stp files"""

        os.system('rm dagmc.cub')

        cad_to_h5m(
            files_with_tags=[
                {
                    'filename':'fusion_example_for_openmc_using_paramak-0.0.1/stp_files/blanket.stp',
                    'material_tag': 'mat1'
                }
            ],
            # h5m_filename='dagmc.h5m',
            # cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
            # surface_reflectivity_name='reflective',
            # merge_tolerance=1e-4,
            cubit_filename='dagmc.cub',
            # geometry_details_filename='geometry_details.json',
            # faceting_tolerance=1.0e-2,
            # make_watertight=True,
        )

        assert Path('dagmc.cub').is_file()
