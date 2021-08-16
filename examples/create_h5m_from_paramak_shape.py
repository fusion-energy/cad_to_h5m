import paramak

shape = paramak.Plasma(
    major_radius=620,
    minor_radius=210,
    triangularity=0.33,
    elongation=1.85,
    rotation_angle=90,
)

# this function makes up of cad_to_h5m within the paramak
my_reactor.export_h5m_with_cubit()
