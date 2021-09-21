import sys
import os
import json
from typing import Dict, List, TypedDict, Optional
from pathlib import Path


class FilesWithTags(TypedDict, total=False):
    filename: str
    material_tag: str
    tet_mesh: str
    scale: float


def cad_to_h5m(
    files_with_tags: FilesWithTags,
    h5m_filename: str = "dagmc.h5m",
    cubit_path: str = "/opt/Coreform-Cubit-2021.5/bin/",
    cubit_filename: Optional[str] = None,
    merge_tolerance: float = 1e-4,
    faceting_tolerance: float = 1.0e-2,
    make_watertight: bool = True,
    imprint: bool = True,
    geometry_details_filename: Optional[str] = None,
    surface_reflectivity_name: str = "reflective",
    exo_filename: Optional[str] = None,
    implicit_complement_material_tag: Optional[str] = None
):
    """Converts a CAD files in STP or SAT format into a h5m file for use in
    DAGMC simulations. The h5m file contains material tags associated with the
    CAD files.

    files_with_tags: The file names of the input CAD files with associated
        materials tags in the form of a list of dictionaries were each
        dictionary has a "cad_filename" and "material_tag" key. For example
        [{"material_tag": "mat1", "cad_filename": "part1.stp"}, {"material_tag":
        "mat2", "cad_filename": "part2.stp"}]. There is also an option to create
        a tet mesh of entries by including a "tet_mesh" key in the dictionary.
        The value is passed to the Cubit mesh command. An example entry would be
        "tet_mesh": "size 0.5". The scale key can also be included to scale up
        or down the geometry so that it is in cm units as required by most
        particle transport codes. And example entry would be "scale": 10 which
        would make the geometry 10 times bigger.
    h5m_filename: the file name of the output h5m file which is suitable for
        use in DAGMC enabled particle transport codes.
    cubit_filename: the file name of the output cubit file. Should end with .cub
        or .cub5. Includes any tet meshes produced and therefore this output
        can be useful for producing unstructured meshes for use in DAGMC
        simulations.
    cubit_path: the path to the Cubit directory used to import Cubit from. On
        Ubuntu with Cubit 2021.5 this would be "/opt/Coreform-Cubit-2021.5/bin/"
    merge_tolerance: The merge tolerance to apply when merging surfaces into
        one.
    faceting_tolerance: The faceting tolerance to apply when faceting edges. Use
        a faceting_tolerance 1.0e-4
    make_watertight: flag to control if the geometry is made watertight prior to
        exporting the h5m file
    imprint: flag to control if the geometry is imprinted prior to exporting
        the h5m file
    geometry_details_filename: The filename to use when saving the geometry
        details. This include linkages between volume numbers, material tags and
        CAD file names. This can be useful for finding the volume number to
        perform a neutronics tally on.
    surface_reflectivity_name: The DAGMC tag name to associate with reflecting
        surfaces. This changes for some neutronics codes but is "reflective"
        in OpenMC and MCNP.
    implicit_complement_material_tag: Material tag to be assigned to the
        implicit complement. Defaults to vacuum.
    """

    if h5m_filename is None or Path(h5m_filename).suffix == ".h5m":
        pass
    else:
        msg = (
            'The h5m_filename argument should end with ".h5m". The provided '
            f'h5m_filename "{h5m_filename}" does not end with .h5m')
        raise ValueError(msg)

    if exo_filename is None or Path(exo_filename).suffix == ".exo":
        pass
    else:
        msg = (
            'The exo_filename argument should end with ".exo". The provided '
            f'exo_filename "{exo_filename}" does not end with .exo')
        raise ValueError(msg)

    if cubit_filename is None or Path(cubit_filename).suffix in [
            ".cub", ".cub5"]:
        pass
    else:
        msg = (
            'The cubit_filename argument should end with ".cub" or ".cub5". '
            f'The provided cubit_filename "{cubit_filename}" does not end '
            ' with either')
        raise ValueError(msg)

    sys.path.append(cubit_path)

    try:
        import cubit
    except ImportError:
        msg = (
            "import cubit failed, cubit was not importable from the "
            f"provided path {cubit_path}"
        )
        raise ImportError(msg)

    cubit.init([])

    geometry_details, total_number_of_volumes = find_number_of_volumes_in_each_step_file(
        files_with_tags, cubit)
    print(geometry_details)

    scale_geometry(geometry_details, cubit)

    tag_geometry_with_mats(
        geometry_details, implicit_complement_material_tag, cubit
    )

    if imprint and total_number_of_volumes > 1:
        imprint_geometry(cubit)
    if total_number_of_volumes > 1:
        merge_geometry(merge_tolerance, cubit)

    # TODO method requires further testing
    find_reflecting_surfaces_of_reflecting_wedge(
        geometry_details, surface_reflectivity_name, cubit
    )

    save_output_files(
        make_watertight,
        geometry_details,
        h5m_filename,
        cubit_filename,
        geometry_details_filename,
        faceting_tolerance,
        exo_filename,
        cubit,
    )
    return h5m_filename


def create_tet_mesh(geometry_details, cubit):
    cubit.cmd("Trimesher volume gradation 1.3")

    cubit.cmd("volume all size auto factor 5")
    for entry in geometry_details:
        if "tet_mesh" in entry.keys():
            for volume in entry["volumes"]:
                cubit.cmd(
                    "volume " + str(volume) + " size auto factor 6"
                )  # this number is the size of the mesh 1 is small 10 is large
                cubit.cmd("volume all scheme tetmesh proximity layers off")
                # example entry ' size 0.5'
                cubit.cmd(f"volume {volume} " + entry["tet_mesh"])
                cubit.cmd("mesh volume " + str(volume))


def scale_geometry(geometry_details: dict, cubit):
    for entry in geometry_details:
        if 'scale' in entry.keys():
            cubit.cmd(
                f'volume {" ".join(entry["volumes"])}  scale  {entry["scale"]}')

# TODO implent a flag to allow tet file info to be saved
# def save_tet_details_to_json_file(
#         geometry_details,
#         filename="mesh_details.json"):
#     for entry in geometry_details:
#         material = entry["material"]
#     tets_in_volumes = cubit.parse_cubit_list(
#         "tet", " in volume " + " ".join(entry["volumes"])
#     )
#     print("material ", material, " has ", len(tets_in_volumes), " tets")
#     entry["tet_ids"] = tets_in_volumes
#     with open(filename, "w") as outfile:
#         json.dump(geometry_details, outfile, indent=4)


def save_output_files(
    make_watertight: bool,
    geometry_details: dict,
    h5m_filename: str,
    cubit_filename: str,
    geometry_details_filename: str,
    faceting_tolerance: float,
    exo_filename: str,
    cubit,
):
    """This saves the output files"""
    cubit.cmd("set attribute on")
    # use a faceting_tolerance 1.0e-4 or smaller for accurate simulations
    if geometry_details_filename is not None:
        with open(geometry_details_filename, "w") as outfile:
            json.dump(geometry_details, outfile, indent=4)

    Path(h5m_filename).parents[0].mkdir(parents=True, exist_ok=True)

    print("using faceting_tolerance of ", faceting_tolerance)
    if make_watertight:
        cubit.cmd(
            'export dagmc "'
            + h5m_filename
            + '" faceting_tolerance '
            + str(faceting_tolerance)
            + " make_watertight"
        )
    else:
        cubit.cmd(
            'export dagmc "'
            + h5m_filename
            + '" faceting_tolerance '
            + str(faceting_tolerance)
        )

    create_tet_mesh(geometry_details, cubit)

    if exo_filename is not None:
        Path(exo_filename).parents[0].mkdir(parents=True, exist_ok=True)
        cubit.cmd(f'export mesh "{exo_filename}" overwrite')

    if cubit_filename is not None:
        cubit.cmd('save as "' + cubit_filename + '" overwrite')

    return h5m_filename


def imprint_geometry(cubit):
    cubit.cmd("imprint body all")


def merge_geometry(merge_tolerance: float, cubit):
    """merges the geometry with te specified tolerance

    Args:
        merge_tolerance: The allowable distance between surfaces before merging
            them together. Optional as there is a default built into the DAGMC
            export command
    """
    cubit.cmd(f"merge tolerance {merge_tolerance}")
    cubit.cmd("merge vol all group_results")


def find_all_surfaces_of_reflecting_wedge(new_vols, cubit):
    surfaces_in_volume = cubit.parse_cubit_list(
        "surface", " in volume " + " ".join(new_vols)
    )
    surface_info_dict = {}
    for surface_id in surfaces_in_volume:
        surface = cubit.surface(surface_id)
        # area = surface.area()
        vertex_in_surface = cubit.parse_cubit_list(
            "vertex", " in surface " + str(surface_id)
        )
        if surface.is_planar() and len(vertex_in_surface) == 4:
            surface_info_dict[surface_id] = {"reflector": True}
        else:
            surface_info_dict[surface_id] = {"reflector": False}
    print("surface_info_dict", surface_info_dict)
    return surface_info_dict


def find_reflecting_surfaces_of_reflecting_wedge(
    geometry_details, surface_reflectivity_name, cubit
):
    print("running find_reflecting_surfaces_of_reflecting_wedge")
    wedge_volume = None
    for entry in geometry_details:
        print(entry)
        print(entry.keys())
        if "surface_reflectivity" in entry.keys():
            print("found surface_reflectivity")
            surface_info_dict = entry["surface_reflectivity"]
            wedge_volume = " ".join(entry["volumes"])
            print("wedge_volume", wedge_volume)
            surfaces_in_wedge_volume = cubit.parse_cubit_list(
                "surface", " in volume " + str(wedge_volume)
            )
            print("surfaces_in_wedge_volume", surfaces_in_wedge_volume)
            for surface_id in surface_info_dict.keys():
                if surface_info_dict[surface_id]["reflector"]:
                    print(
                        surface_id,
                        "surface originally reflecting but does it still exist",
                    )
                    if surface_id not in surfaces_in_wedge_volume:
                        del surface_info_dict[surface_id]
            for surface_id in surfaces_in_wedge_volume:
                if surface_id not in surface_info_dict.keys():
                    surface_info_dict[surface_id] = {"reflector": True}
                    cubit.cmd(
                        'group "'
                        + surface_reflectivity_name
                        + '" add surf '
                        + str(surface_id)
                    )
                    cubit.cmd("surface " + str(surface_id) + " visibility on")
            entry["surface_reflectivity"] = surface_info_dict
            return geometry_details, wedge_volume
    return geometry_details, wedge_volume


def tag_geometry_with_mats(
    geometry_details, implicit_complement_material_tag, cubit
):
    for entry in geometry_details:
        if "material_tag" in entry.keys():

            if len(entry['material_tag']) > 27:
                msg = ("material_tag > 28 characters. Material tags "
                       "must be less than 28 characters use in DAGMC. "
                       f"{entry['material_tag']} is too long.")
                raise ValueError(msg)

            cubit.cmd(
                'group "mat:'
                + str(entry["material_tag"])
                + '" add volume '
                + " ".join(entry["volumes"])
            )
            if entry['material_tag'].lower() == 'graveyard':
                if implicit_complement_material_tag is not None:
                    graveyard_volume_number = entry["volumes"][0]
                    cubit.cmd(
                        f'group "mat:{implicit_complement_material_tag}_comp" add vol {graveyard_volume_number}'
                    )
        else:
            msg = f"dictionary key material_tag is missing for {entry}"
            raise ValueError(msg)


def find_number_of_volumes_in_each_step_file(files_with_tags, cubit):
    """ """
    for entry in files_with_tags:
        print(f'loading {entry["cad_filename"]}')
        current_vols = cubit.parse_cubit_list("volume", "all")
        if entry["cad_filename"].endswith(
                ".stp") or entry["cad_filename"].endswith(".step"):
            import_type = "step"
        elif entry["cad_filename"].endswith(".sat"):
            import_type = "acis"
        else:
            msg = (f'File format for {entry["cad_filename"]} is not supported.'
                   'Try step files or sat files')
            raise ValueError(msg)
        if not Path(entry["cad_filename"]).is_file():
            msg = f'File with filename {entry["cad_filename"]} could not be found'
            raise FileNotFoundError(msg)
        short_file_name = os.path.split(entry["cad_filename"])[-1]
        cubit.cmd(
            "import "
            + import_type
            + ' "'
            + entry["cad_filename"]
            + '" separate_bodies no_surfaces no_curves no_vertices '
        )
        all_vols = cubit.parse_cubit_list("volume", "all")
        new_vols = set(current_vols).symmetric_difference(set(all_vols))
        new_vols = list(map(str, new_vols))
        if len(new_vols) > 1:
            cubit.cmd(
                "unite vol " +
                " ".join(new_vols) +
                " with vol " +
                " ".join(new_vols))
        all_vols = cubit.parse_cubit_list("volume", "all")
        new_vols_after_unite = set(
            current_vols).symmetric_difference(set(all_vols))
        new_vols_after_unite = list(map(str, new_vols_after_unite))
        entry["volumes"] = new_vols_after_unite
        cubit.cmd(
            'group "' +
            short_file_name +
            '" add volume ' +
            " ".join(
                entry["volumes"]))
        if "surface_reflectivity" in entry.keys():
            entry["surface_reflectivity"] = find_all_surfaces_of_reflecting_wedge(
                new_vols_after_unite, cubit)
            print(
                "entry['surface_reflectivity']",
                entry["surface_reflectivity"])
    cubit.cmd("separate body all")

    # checks the cad is clean and catches some errors with the geometry early
    cubit.cmd("validate vol all")
    cubit.cmd("autoheal analyze vol all")

    return files_with_tags, sum(all_vols)
