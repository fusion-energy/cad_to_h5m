import os
import tarfile
import unittest
import urllib.request
from pathlib import Path

import pytest
from cad_to_h5m import cad_to_h5m


class TestApiUsage(unittest.TestCase):
    def setUp(self):

        if not Path("tests/v0.0.1.tar.gz").is_file():
            url = "https://github.com/Shimwell/fusion_example_for_openmc_using_paramak/archive/refs/tags/v0.0.1.tar.gz"
            urllib.request.urlretrieve(url, "tests/v0.0.1.tar.gz")

        tar = tarfile.open("tests/v0.0.1.tar.gz", "r:gz")
        tar.extractall("tests")
        tar.close()

    def test_h5m_file_creation(self):
        """Checks that a h5m file is created from stp files when make_watertight
        is set to false"""

        os.system("rm test_dagmc.h5m")

        test_h5m_filename = "test_dagmc.h5m"

        returned_filename = cad_to_h5m(
            files_with_tags=[
                {
                    "filename": "tests/fusion_example_for_openmc_using_paramak-0.0.1/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }
            ],
            h5m_filename=test_h5m_filename,
            # cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
            # surface_reflectivity_name='reflective',
            # merge_tolerance=1e-4,
            # cubit_filename='dagmc.cub',
            # geometry_details_filename='geometry_details.json',
            # faceting_tolerance=1.0e-2,
            make_watertight=False,
        )

        assert Path(test_h5m_filename).is_file()
        assert Path(returned_filename).is_file()
        assert test_h5m_filename == returned_filename

    def test_watertight_h5m_file_creation(self):
        """Checks that a h5m file is created from stp files"""

        os.system("rm dagmc.h5m")

        cad_to_h5m(
            files_with_tags=[
                {
                    "filename": "tests/fusion_example_for_openmc_using_paramak-0.0.1/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }],
            h5m_filename="dagmc.h5m",
            make_watertight=True,
        )

        assert Path("dagmc.h5m").is_file()

    def test_cub_file_creation(self):
        """Checks that a h5m file is created from stp files"""

        os.system("rm dagmc.cub")

        cad_to_h5m(
            files_with_tags=[
                {
                    "filename": "tests/fusion_example_for_openmc_using_paramak-0.0.1/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }],
            cubit_filename="dagmc.cub",
        )

        assert Path("dagmc.cub").is_file()

    def test_faceting_tolerance_increases_file_size(self):
        """Checks that a h5m file is created from stp files"""

        os.system("rm *.h5m")

        cad_to_h5m(
            files_with_tags=[
                {
                    "filename": "tests/fusion_example_for_openmc_using_paramak-0.0.1/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }],
            h5m_filename="dagmc_default_faceting_tolerance.h5m",
            faceting_tolerance=1.0e-2,
        )

        assert Path("dagmc_default_faceting_tolerance.h5m").is_file()

        cad_to_h5m(
            files_with_tags=[
                {
                    "filename": "tests/fusion_example_for_openmc_using_paramak-0.0.1/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }],
            h5m_filename="dagmc_small_faceting_tolerance.h5m",
            faceting_tolerance=0.5e-2,
        )

        assert Path("dagmc_small_faceting_tolerance.h5m").is_file()

        assert (
            Path("dagmc_small_faceting_tolerance.h5m").stat().st_size
            > Path("dagmc_default_faceting_tolerance.h5m").stat().st_size
        )
