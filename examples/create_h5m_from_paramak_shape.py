
import paramak

shape = paramak.Plasma(
    major_radius=620,
    minor_radius=210,
    triangularity=0.33,
    elongation=1.85,
    rotation_angle=90,
)

print(shape.neutronics_description())
shape.export_h5m_with_cubit()