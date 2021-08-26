import paramak
from cad_to_h5m import cad_to_h5m

my_shape = paramak.Plasma(
    major_radius=620,
    minor_radius=210,
    triangularity=0.33,
    elongation=1.85,
    rotation_angle=90,
)

my_shape.export_stp()

files_with_tags = my_shape.neutronics_description()

cad_to_h5m(
    h5m_filename=' "dagmc.h5m',
    cubit_path="/opt/Coreform-Cubit-2021.5/bin/",
    files_with_tags=files_with_tags
)
