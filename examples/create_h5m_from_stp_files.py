
from cad_to_h5m import cad_to_h5m
import urllib.request


# import paramak

# my_reactor = paramak.SubmersionTokamak(
#     inner_bore_radial_thickness=30,
#     inboard_tf_leg_radial_thickness=30,
#     center_column_shield_radial_thickness=30,
#     divertor_radial_thickness=80,
#     inner_plasma_gap_radial_thickness=50,
#     plasma_radial_thickness=200,
#     outer_plasma_gap_radial_thickness=50,
#     firstwall_radial_thickness=30,
#     blanket_rear_wall_radial_thickness=30,
#     number_of_tf_coils=16,
#     rotation_angle=90,
#     support_radial_thickness=90,
#     inboard_blanket_radial_thickness=30,
#     outboard_blanket_radial_thickness=30,
#     elongation=2.00,
#     triangularity=0.50,
#     pf_coil_case_thicknesses=[10, 10, 10, 10],
#     pf_coil_radial_thicknesses=[20, 50, 50, 20],
#     pf_coil_vertical_thicknesses=[20, 50, 50, 20],
#     pf_coil_radial_position=[500, 550, 550, 500],
#     pf_coil_vertical_position=[270, 100, -100, -270],
#     rear_blanket_to_tf_gap=50,
#     outboard_tf_coil_radial_thickness=30,
#     outboard_tf_coil_poloidal_thickness=30,
# )

# my_reactor.export_stp()

# url = 'https://raw.githubusercontent.com/Shimwell/fusion_example_for_openmc_using_paramak/main/stp_files/blanket.stp'
# urllib.request.urlretrieve(url, 'blanket.stp')

cad_to_h5m(
    files_with_tags=[
        {
            "material_tag": "pf_coil_mat",
            "filename": "pf_coils.stp",
        },
        {
            "material_tag": "pf_coil_case_mat",
            "filename": "pf_coil_cases.stp",
        },
        {
            "material_tag": "center_column_shield_mat",
            "filename": "center_column_shield.stp",
        },
        {
            "material_tag": "firstwall_mat",
            "filename": "outboard_firstwall.stp",
        },
        {
            "material_tag": "blanket_mat",
            "filename": "blanket.stp",
        },
        {
            "material_tag": "divertor_mat",
            "filename": "divertor.stp",
        },
        {
            "material_tag": "supports_mat",
            "filename": "supports.stp",
        },
        {
            "material_tag": "blanket_rear_wall_mat",
            "filename": "outboard_rear_blanket_wall.stp",
        },
        {
            "material_tag": "inboard_tf_coils_mat",
            "filename": "inboard_tf_coils.stp",
        },
        {
            "material_tag": "outer_tf_coil_mat",
            "filename": "outboard_tf_coil.stp",
        },
        {
            "material_tag": "graveyard",
            "filename": "graveyard.stp",
        },
        {
            "material_tag": "vacuum",
            "filename": "sector_wedge.stp",
            "surface_reflectivity": True,
        }
    ],
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
)
