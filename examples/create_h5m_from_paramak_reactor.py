import paramak

my_reactor = paramak.BallReactor(
    inner_bore_radial_thickness=10,
    inboard_tf_leg_radial_thickness=30,
    center_column_shield_radial_thickness=60,
    divertor_radial_thickness=150,
    inner_plasma_gap_radial_thickness=30,
    plasma_radial_thickness=300,
    outer_plasma_gap_radial_thickness=30,
    firstwall_radial_thickness=30,
    blanket_radial_thickness=50,
    blanket_rear_wall_radial_thickness=30,
    elongation=2,
    triangularity=0.55,
    number_of_tf_coils=16,
    rotation_angle=90,
    pf_coil_case_thicknesses=[10, 10, 10, 10],
    pf_coil_radial_thicknesses=[20, 50, 50, 20],
    pf_coil_vertical_thicknesses=[20, 50, 50, 20],
    pf_coil_radial_position=[500, 575, 575, 500],
    pf_coil_vertical_position=[300, 100, -100, -300],
    rear_blanket_to_tf_gap=50,
    outboard_tf_coil_radial_thickness=100,
    outboard_tf_coil_poloidal_thickness=50,
)

# this function makes up of cad_to_h5m within the paramak
my_reactor.export_h5m_with_cubit()
