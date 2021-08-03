
from cad_to_h5m import cad_to_h5m
import urllib.request

cd 

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
            # "surface_reflectivity": True,
        }
    ],
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/'
)
