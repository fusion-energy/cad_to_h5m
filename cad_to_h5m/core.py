import sys
import os
import json

def cad_to_h5m(
    files_with_tags,
    h5m_filename='dagmc.h5m',
    cubit_path='/opt/Coreform-Cubit-2021.5/bin/',
    surface_reflectivity_name='reflective',
    merge_tolerance=1e4,
    cubit_filename='dagmc.cub',
    geometry_details_filename='geometry_details.json',
    faceting_tolerance=1.0e-2,
    make_watertight=True,
):

    sys.path.append(cubit_path)
    import cubit
    cubit.init([])
    geometry_details = find_number_of_volumes_in_each_step_file(files_with_tags, cubit)
    print(geometry_details)
    tag_geometry_with_mats(geometry_details, cubit)

    imprint_and_merge_geometry(merge_tolerance, cubit)
    find_reflecting_surfaces_of_reflecting_wedge(geometry_details, surface_reflectivity_name, cubit)
    save_output_files(make_watertight, geometry_details, h5m_filename, cubit_filename, geometry_details_filename, faceting_tolerance, cubit)

def save_output_files(make_watertight, geometry_details, h5m_filename, cubit_filename, geometry_details_filename, faceting_tolerance, cubit):
    """This saves the output files"""
    cubit.cmd("set attribute on")
    # use a faceting_tolerance 1.0e-4 or smaller for accurate simulations
    print('using faceting_tolerance of ', faceting_tolerance)
    if make_watertight == True:
        cubit.cmd('export dagmc "'+h5m_filename+'" faceting_tolerance '+ str(faceting_tolerance) + ' make_watertight')
    else:
        cubit.cmd('export dagmc "'+h5m_filename+'" faceting_tolerance '+ str(faceting_tolerance))

    # os.system('mbconvert -1 '+h5m_filename+' dagmc_not_watertight_edges.h5m')
    if cubit_filename is not None:
        cubit.cmd('save as "'+cubit_filename+'" overwrite')
    # if trelis_filename is not None:
    #     cubit.cmd('save as "'+trelis_filename+'" overwrite')
    if geometry_details_filename is not None:
        with open(geometry_details_filename, "w") as outfile:
            json.dump(geometry_details, outfile, indent=4)


def imprint_and_merge_geometry(merge_tolerance, cubit):
    cubit.cmd("imprint body all")
    print('using merge_tolerance of ', str(merge_tolerance))
    cubit.cmd("merge tolerance " + str(merge_tolerance))  # optional as there is a default
    cubit.cmd("merge vol all group_results")
    cubit.cmd("graphics tol angle 3")


def find_all_surfaces_of_reflecting_wedge(new_vols, cubit):
    surfaces_in_volume = cubit.parse_cubit_list("surface", " in volume "+' '.join(new_vols))
    surface_info_dict = {}
    for surface_id in surfaces_in_volume:
        surface = cubit.surface(surface_id)
        #area = surface.area()
        vertex_in_surface = cubit.parse_cubit_list("vertex", " in surface " + str(surface_id))
        if surface.is_planar() == True and len(vertex_in_surface) == 4:
            surface_info_dict[surface_id] = {'reflector': True}
        else:
            surface_info_dict[surface_id] = {'reflector': False}
    print('surface_info_dict', surface_info_dict)
    return surface_info_dict

def find_reflecting_surfaces_of_reflecting_wedge(geometry_details, surface_reflectivity_name, cubit):
    print('running find_reflecting_surfaces_of_reflecting_wedge')
    wedge_volume = None
    for entry in geometry_details:
        print(entry)
        print(entry.keys())
        if 'surface_reflectivity' in entry.keys():
            print('found surface_reflectivity')
            surface_info_dict = entry['surface_reflectivity']
            wedge_volume = ' '.join(entry['volumes'])
            print('wedge_volume', wedge_volume)
            surfaces_in_wedge_volume = cubit.parse_cubit_list("surface", " in volume "+str(wedge_volume))
            print('surfaces_in_wedge_volume', surfaces_in_wedge_volume)
            for surface_id in surface_info_dict.keys():
                if surface_info_dict[surface_id]['reflector'] == True:
                    print(surface_id, 'surface originally reflecting but does it still exist')
                    if surface_id not in surfaces_in_wedge_volume:
                        del surface_info_dict[surface_id]
            for surface_id in surfaces_in_wedge_volume:
                if surface_id not in surface_info_dict.keys():
                    surface_info_dict[surface_id] = {'reflector': True}
                    cubit.cmd('group "' + surface_reflectivity_name + '" add surf ' + str(surface_id))
                    cubit.cmd('surface ' + str(surface_id)+' visibility on')
            entry['surface_reflectivity'] = surface_info_dict
            return geometry_details, wedge_volume
    return geometry_details, wedge_volume

def tag_geometry_with_mats(geometry_details, cubit):
    for entry in geometry_details:
        if 'material_tag' in entry.keys():
            cubit.cmd(
                'group "mat:'
                + str(entry['material_tag'])
                + '" add volume '
                + " ".join(entry["volumes"])
            )
        else:
            print('material_key_name', 'material_tag', 'not found for', entry)

def find_number_of_volumes_in_each_step_file(files_with_tags, cubit):
    """
    """
    body_ids = ""
    volumes_in_each_step_file = []
    # all_groups=cubit.parse_cubit_list("group","all")
    # starting_group_id = len(all_groups)
    for entry in files_with_tags:
        # starting_group_id = starting_group_id +1
        current_vols = cubit.parse_cubit_list("volume", "all")
        #print(os.path.join(basefolder, entry['filename']))
        if entry['filename'].endswith(".sat"):
            import_type = "acis"
        if entry['filename'].endswith(
                ".stp") or entry['filename'].endswith(".step"):
            import_type = "step"
        short_file_name = os.path.split(entry['filename'])[-1]
        # print('short_file_name',short_file_name)
        # cubit.cmd('import '+import_type+' "' + entry['stp_filename'] + '" separate_bodies no_surfaces no_curves no_vertices group "'+str(short_file_name)+'"')
        cubit.cmd(
            "import "
            + import_type
            + ' "'
            + entry['filename']
            + '" separate_bodies no_surfaces no_curves no_vertices '
        )
        all_vols = cubit.parse_cubit_list("volume", "all")
        new_vols = set(current_vols).symmetric_difference(set(all_vols))
        new_vols = list(map(str, new_vols))
        print("new_vols", new_vols, type(new_vols))
        current_bodies = cubit.parse_cubit_list("body", "all")
        print("current_bodies", current_bodies)
        # volumes_in_group = cubit.cmd('volume in group '+str(starting_group_id))
        # print('volumes_in_group',volumes_in_group,type(volumes_in_group))
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
        if 'surface_reflectivity' in entry.keys():
            entry['surface_reflectivity'] = find_all_surfaces_of_reflecting_wedge(new_vols_after_unite, cubit)
            print("entry['surface_reflectivity']", entry['surface_reflectivity'])
    cubit.cmd("separate body all")
    return files_with_tags
