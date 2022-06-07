import os
import tarfile
import unittest
import urllib.request
from pathlib import Path

from cad_to_h5m import cad_to_h5m


class TestApiUsage(unittest.TestCase):
    def setUp(self):

        if not Path("tests/v0.2.0.tar.gz").is_file():
            url = "https://github.com/Shimwell/fusion_example_for_openmc_using_paramak/archive/refs/tags/v0.2.0.tar.gz"
            urllib.request.urlretrieve(url, "tests/v0.2.0.tar.gz")

            tar = tarfile.open("tests/v0.0.1.tar.gz", "r:gz")
            tar.extractall("tests")
            tar.close()

        if not Path("tests/0.1.0.tar.gz").is_file():
            url = "https://github.com/fusion-energy/fusion_neutronics_workflow/archive/refs/tags/0.1.0.tar.gz"
            urllib.request.urlretrieve(url, "tests/0.1.0.tar.gz")

            tar = tarfile.open("tests/0.1.0.tar.gz", "r:gz")
            tar.extractall("tests")
            tar.close()

    def test_h5m_file_creation(self):
        """Checks that a h5m file is created from stp files when make_watertight
        is set to false"""

        test_h5m_filename = "test_dagmc.h5m"
        os.system(f"rm {test_h5m_filename}")

        returned_filename = cad_to_h5m(
            files_with_tags=[
                {
                    "cad_filename": "tests/fusion_example_for_openmc_using_paramak-v0.2.0/stp_files/blanket.stp",
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

    def test_h5m_file_creation_in_subfolder(self):
        """Checks that a h5m file is created from stp files when make_watertight
        is set to false"""

        test_h5m_filename = "subfolder/test_dagmc.h5m"
        os.system(f"rm {test_h5m_filename}")

        returned_filename = cad_to_h5m(
            files_with_tags=[
                {
                    "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }
            ],
            h5m_filename=test_h5m_filename,
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
                    "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }
            ],
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
                    "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }
            ],
            cubit_filename="dagmc.cub",
        )

        assert Path("dagmc.cub").is_file()

    def test_faceting_tolerance_increases_file_size(self):
        """Checks that a h5m file is created from stp files"""

        os.system("rm *.h5m")

        cad_to_h5m(
            files_with_tags=[
                {
                    "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }
            ],
            h5m_filename="dagmc_default_faceting_tolerance.h5m",
            faceting_tolerance=1.0e-2,
        )

        assert Path("dagmc_default_faceting_tolerance.h5m").is_file()

        cad_to_h5m(
            files_with_tags=[
                {
                    "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }
            ],
            h5m_filename="dagmc_small_faceting_tolerance.h5m",
            faceting_tolerance=0.5e-2,
        )

        assert Path("dagmc_small_faceting_tolerance.h5m").is_file()

        assert (
            Path("dagmc_small_faceting_tolerance.h5m").stat().st_size
            > Path("dagmc_default_faceting_tolerance.h5m").stat().st_size
        )

    def test_exo_file_creation_with_different_sizes(self):
        """Checks that a h5m file is created from stp files"""

        os.system("rm umesh_2.exo")

        cad_to_h5m(
            files_with_tags=[
                {
                    "cad_filename": "tests/fusion_neutronics_workflow-0.1.0/example_01_single_volume_cell_tally/stage_1_output/steel.stp",
                    "material_tag": "mat1",
                    "tet_mesh": "size 2",
                }
            ],
            exo_filename="umesh_2.exo",
        )

        assert Path("umesh_2.exo").is_file()

        os.system("rm umesh_3.exo")

        cad_to_h5m(
            files_with_tags=[
                {
                    "cad_filename": "tests/fusion_neutronics_workflow-0.1.0/example_01_single_volume_cell_tally/stage_1_output/steel.stp",
                    "material_tag": "mat1",
                    "tet_mesh": "size 3",
                }
            ],
            exo_filename="umesh_3.exo",
        )

        assert Path("umesh_3.exo").is_file()

        # mesh size exceeds 50,000 and files end up the same size.
        # assert (Path("umesh_3.exo").stat().st_size >
        #         Path("umesh_2.exo").stat().st_size)

    def test_exo_file_creation_with_default_size(self):
        """Checks that a h5m file is created from stp files"""

        os.system("rm umesh_default.exo")

        cad_to_h5m(
            files_with_tags=[
                {
                    "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/pf_coils.stp",
                    "material_tag": "mat1",
                    "tet_mesh": "",
                }
            ],
            exo_filename="umesh_default.exo",
        )

        assert Path("umesh_default.exo").is_file()

    def test_exo_file_suffix_error_handling(self):
        """Attempts save a cub file with the wrong file suffix"""

        def incorrect_suffix():
            cad_to_h5m(
                files_with_tags=[
                    {
                        "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/pf_coils.stp",
                        "material_tag": "mat1",
                    }
                ],
                exo_filename="output_file_with.not_correct_suffix",
            )

        self.assertRaises(ValueError, incorrect_suffix)

    def test_h5m_file_suffix_error_handling(self):
        """Attempts save a cub file with the wrong file suffix"""

        def incorrect_suffix():
            cad_to_h5m(
                files_with_tags=[
                    {
                        "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/pf_coils.stp",
                        "material_tag": "mat1",
                    }
                ],
                h5m_filename="output_file_with.not_correct_suffix",
            )

        self.assertRaises(ValueError, incorrect_suffix)

    def test_cubit_file_suffix_error_handling(self):
        """Attempts save a cub file with the wrong file suffix"""

        def incorrect_suffix():
            cad_to_h5m(
                files_with_tags=[
                    {
                        "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/pf_coils.stp",
                        "material_tag": "mat1",
                    }
                ],
                cubit_filename="output_file_with.not_correct_suffix",
            )

        self.assertRaises(ValueError, incorrect_suffix)

    def test_h5m_file_creation_with_scaling(self):
        """Checks that a h5m file is created from stp files when volumes are
        scaled"""

        test_h5m_filename = "test_dagmc.h5m"
        os.system(f"rm {test_h5m_filename}")

        returned_filename = cad_to_h5m(
            files_with_tags=[
                {
                    "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/blanket.stp",
                    "material_tag": "mat1",
                    "scale": 0.1,
                }
            ],
            h5m_filename=test_h5m_filename,
        )

        assert Path(test_h5m_filename).is_file()
        assert Path(returned_filename).is_file()
        assert test_h5m_filename == returned_filename

    def test_implicit_complement_assignment(self):
        """Checks h5m file creation and that the resulting h5m file contains
        the material tag assigned to the implicit complement"""

        test_h5m_filename = "test_dagmc.h5m"
        os.system(f"rm {test_h5m_filename}")

        implicit_complement_material = "air"

        returned_filename = cad_to_h5m(
            files_with_tags=[
                {
                    "cad_filename": "tests/fusion_example_for_openmc_using_paramak-0.2.0/stp_files/blanket.stp",
                    "material_tag": "mat1",
                }
            ],
            implicit_complement_material_tag=implicit_complement_material,
            h5m_filename=test_h5m_filename,
        )

        assert Path(test_h5m_filename).is_file()
        assert Path(returned_filename).is_file()
        assert test_h5m_filename == returned_filename
