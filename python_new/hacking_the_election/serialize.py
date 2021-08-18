"""
Script for serializing block-level election, geo, and population data.
Data is serialized into ".pickle" file containing graph with nodes containing Precinct objects

Usage (from the python directory):
python3 -m hacking_the_election.serialize [state_name] [(optional) check_point]
"""
import sys
import json
# from types import new_class
import time
import pandas
import subprocess
from os.path import dirname, abspath
from os import listdir
import pickle
from itertools import combinations

import networkx as nx
from networkx.algorithms import (
    connected_components,
    number_connected_components
)
from shapely.geometry import Point, MultiPolygon, Polygon

from hacking_the_election.utils.precinct import Precinct
from hacking_the_election.utils.block import Block
from hacking_the_election.utils.geometry import geojson_to_shapely, get_if_bordering, shapely_to_geojson
from hacking_the_election.visualization.graph_visualization import visualize_graph

def fractional_assignment(racial_data):
    """
    Weights are based off of "A Practical Approach to Using Multiple-Race Response Data", 
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2831381/
    """
    keys = list(racial_data.keys())
    for key in keys:
        # Get rid of multi-race categories with other in them
        if key.endswith("other"):
            if key != "other":
                racial_data[key[:-6]] += racial_data[key]
                del racial_data[key]

    keys = list(racial_data.keys())
    for key in keys:
        # Concatcate Asian Americans and Native Hawaiians and other Pacific Islanders
        if key.find("nhpi") != -1:
            if key.find("asian") != -1:
                end_nhpi = key.find("nhpi")+4
                # try:
                #     if key[end_nhpi+1] == ":":
                #         non_nhpi_key = key[:key.find("nhpi")-1] + key[end_nhpi+1:]
                # except:
                non_nhpi_key = key[:-5]
                racial_data[non_nhpi_key] += racial_data[key]
            else:
                non_nhpi_key = key.replace("nhpi", "asian")
                racial_data[non_nhpi_key] += racial_data[key]
            del racial_data[key]
    keys = list(racial_data.keys())
    for key in keys:
        # Rename the Asian category as Asian American and Pacific Islander (AAPI)
        if key.find("asian") != -1:
            aapi_key = key.replace("asian", "aapi")
            racial_data[aapi_key] = racial_data[key]
            del racial_data[key]

    # Apply weights
    racial_data["aian"] += .404*racial_data["aian:aapi"]
    racial_data["aapi"] += .596*racial_data["aian:aapi"]
    del racial_data["aian:aapi"]
    racial_data["aian"] += .186*racial_data["black:aian"]
    racial_data["black"] += .814*racial_data["black:aian"]
    del racial_data["black:aian"]
    racial_data["aian"] += .205*racial_data["white:aian"]
    racial_data["white"] += .795*racial_data["white:aian"]
    del racial_data["white:aian"]
    racial_data["black"] += .621*racial_data["white:black"]
    racial_data["white"] += .379*racial_data["white:black"]
    del racial_data["white:black"]
    racial_data["black"] += .370*racial_data["black:aapi"]
    racial_data["aapi"] += .630*racial_data["black:aapi"]
    del racial_data["black:aapi"]
    racial_data["aapi"] += .327*racial_data["white:aapi"]
    racial_data["white"] += .673*racial_data["white:aapi"]
    del racial_data["white:aapi"]

    racial_data["aian"] += .195*racial_data["white:black:aian"]
    racial_data["black"] += .572*racial_data["white:black:aian"]
    racial_data["white"] += .233*racial_data["white:black:aian"]
    del racial_data["white:black:aian"]
    racial_data["aian"] += .286*racial_data["black:aian:aapi"]
    racial_data["black"] += .461*racial_data["black:aian:aapi"]
    racial_data["aapi"] += .253*racial_data["black:aian:aapi"]
    del racial_data["black:aian:aapi"]
    racial_data["aian"] += .024*racial_data["white:aian:aapi"]
    racial_data["aapi"] += .043*racial_data["white:aian:aapi"]
    racial_data["white"] += .933*racial_data["white:aian:aapi"]
    del racial_data["white:aian:aapi"]
    racial_data["aapi"] += .104*racial_data["white:black:aapi"]
    racial_data["black"] += .113*racial_data["white:black:aapi"]
    racial_data["white"] += .782*racial_data["white:black:aapi"]
    del racial_data["white:black:aapi"]
    racial_data["aian"] += .01*racial_data["white:black:aian:aapi"]
    racial_data["aapi"] += .009*racial_data["white:black:aian:aapi"]
    racial_data["black"] += .02*racial_data["white:black:aian:aapi"]
    racial_data["white"] += .960*racial_data["white:black:aian:aapi"]
    del racial_data["white:black:aian:aapi"] 

def split_multipolygons(block_list):
    indexes_to_remove = []
    blocks_to_add = []
    for i, block in enumerate(block_list):
        if isinstance(block.coords, MultiPolygon):
            indexes_to_remove.append(i)
            full_area = block.coords.area
            for j, polygon in enumerate(block.coords):
                ratio = polygon.area/full_area 
                pop = block.pop * ratio
                state = block.state
                id = block.id + "_s" + str(j)
                split_racial_data = {}
                for race, data in block.racial_data.items():
                    split_racial_data[race] = data * ratio
                split_rep_votes = block.rep_votes * ratio
                split_dem_votes = block.dem_votes * ratio
                split_total_votes = block.total_votes * ratio
                new_split_block = Block(pop, polygon, state, id, split_racial_data, split_total_votes, split_rep_votes, split_dem_votes)
                new_split_block.land = block.land * ratio
                new_split_block.water = block.water * ratio
                # try:
                new_split_block.long = block.long * ratio
                # except:
                    # raise Exception(f"{block.long},{ratio}")
                new_split_block.lat = block.lat * ratio
                new_split_block.area = block.area * ratio
                new_split_block.density = block.density * ratio
                blocks_to_add.append(new_split_block)
    indexes_to_remove.sort(reverse=True)
    for index in indexes_to_remove:
        block_list.pop(index)
    for block in blocks_to_add:
        block_list.append(block)
    print(f"Multipolygons removed: {len(indexes_to_remove)}")
    print(f"New polygons created: {len(blocks_to_add)}")

def combine_holypolygons(block_list):
    # Once these holes have already accounted for (data added to surrounding block, no need to check again)
    # actually stores indexes of holes
    holes = []
    for block in block_list:
        # print(block.id)
        # if block.id == "1000000US500239552003006":
            # print("ok!", list(block.coords.interiors)[0], block.coords)
        if len(list(block.coords.interiors)) > 0:
            hole_area = sum([hole.area for hole in list(block.coords.interiors)])
            found_area = 0
            for i, check_block in enumerate(block_list):
                if check_block.min_x < block.min_x or check_block.max_x > block.max_x or check_block.min_y < block.min_y or check_block.max_y > block.max_y:
                    continue
                if i in holes:
                    continue
                if check_block.id == block.id:
                    continue
                # if found_area > hole_area:
                #     break
                for hole in block.coords.interiors:
                    # if block.id == "1000000US500239552003006":
                    #     print("ok!")
                        # if check_block.id == "1000000US500239552003007":
                            # print("yes!", abs(hole.intersection(check_block.coords).area - check_block.coords.area) <= 0.02*check_block.coords.area)
                            # print(hole.intersection(check_block.coords).area, check_block.coords.area, abs(hole.intersection(check_block.coords).area - check_block.coords.area), 0.02*check_block.coords.area)
                    # if abs(hole.intersection(check_block.coords).area - check_block.coords.area) <= 0.02*check_block.coords.area:
                    if Point(check_block.coords.centroid).within(Polygon(hole)):
                        if block.id == "1000000US500099501001366":
                            if check_block.id == "1000000US500099501001376":
                                print("japan hole is found!")
                            else:
                                print("other holes were found", check_block.id)
                        if block.id == "1000000US500099501001376":
                            print("this is the japan non hole!")
                        # if block.id == "1000000US500199518001036":
                        #     if check_block.id == "1000000US500199518001043":
                        holes.append(i)
                        found_area += check_block.coords.area
                        block.pop += check_block.pop
                        block.land += check_block.land
                        block.water += check_block.water
                        block.long += check_block.long
                        block.lat += check_block.lat
                        block.area += check_block.area
                        block.density += check_block.density
                        # This try/except can be removed once all blocks are matched!
                        try:
                            block.rep_votes += check_block.rep_votes
                            block.dem_votes += check_block.dem_votes
                            block.create_election_data()
                        except:
                            pass
                        for race, data in check_block.racial_data.items():
                            block.racial_data[race] += data
                        block.create_racial_data()
                        break
            block.coords = Polygon(block.coords.exterior)
    holes.sort(reverse=True)
    for index in holes:
        try:
            block_list.pop(index)
        except:
            print(index)

            print("\n")
    print(f"Holes removed: {len(holes)}")

def connect_islands(block_graph):
    original_graph_components_num = number_connected_components(block_graph)
    if not number_connected_components(block_graph) == 1:
        while number_connected_components(block_graph) != 1:
            graph_components = list(connected_components(block_graph))
            # print(graph_components, '# of graph components')
            # Create list with dictionary containing keys as precincts, 
            # values as centroids for each component
            centroid_list = []
            for component in graph_components:
                component_list = {}
                for block in component:
                    component_list[block] = block_graph.nodes[block]['block'].centroid
                centroid_list.append(component_list)
                
            # Keys are minimum distances to and from different islands, 
            # values are tuples of nodes to add edges between
            min_distances = {}
            # print(len(list(combinations([num for num in range(0, len(graph_components))], 2))), 'list of stuffs')
            # For nonrepeating combinations of components, add to list of edges
            for combo in list(combinations([num for num in range(0, (len(graph_components) - 1))], 2)):
                # Create list of centroids to compare
                centroids_1 = centroid_list[combo[0]]
                centroids_2 = centroid_list[combo[1]]
                min_distance = 0
                min_tuple = None
                for block_1, centroid_1 in centroids_1.items():
                    for block_2, centroid_2 in centroids_2.items():
                        x_distance = centroid_1[0] - centroid_2[0]
                        y_distance = centroid_1[1] - centroid_2[1]
                        # No need to sqrt unnecessarily
                        distance = (x_distance ** 2) + (y_distance ** 2)
                        if min_distance == 0:
                            min_distance = distance
                            min_tuple = (block_1, block_2)
                        elif distance < min_distance:
                            # print(block_1, block_2)
                            min_distance = distance
                            min_tuple = (block_1, block_2)
                min_distances[min_distance] = min_tuple
            # combinations() fails once the graph is one edge away from completion, so this is manual
            if len(graph_components) == 2:
                min_distance = 0
                for block_1 in graph_components[0]:
                    centroid_1 = block_graph.nodes[block_1]['block'].centroid
                    for block_2 in graph_components[1]:
                        centroid_2 = block_graph.nodes[block_2]['block'].centroid
                        x_distance = centroid_1[0] - centroid_2[0]
                        y_distance = centroid_1[1] - centroid_2[1]
                        # No need to sqrt unnecessarily
                        distance = (x_distance ** 2) + (y_distance ** 2)
                        if min_distance == 0:
                            min_distance = distance
                            min_tuple = (block_1, block_2)
                        elif distance < min_distance:
                            # print(block_1, block_2)
                            min_distance = distance
                            min_tuple = (block_1, block_2)
                min_distances[min_distance] = min_tuple

            # Find edge to add
            try:
                edge_to_add = min_distances[min(min_distances)]
            except ValueError:
                break
            block_graph.add_edge(*edge_to_add)
            block_graph.nodes[edge_to_add[0]]['block'].neighbors.append(block_graph.nodes[edge_to_add[1]]['block'].id)
            block_graph.nodes[edge_to_add[1]]['block'].neighbors.append(block_graph.nodes[edge_to_add[0]]['block'].id)
            print(f"\rConnecting islands progress: {100 - round(100 * (len(graph_components)-1)/original_graph_components_num, 2)}%")

            # print('yo', block_graph.nodes[edge_to_add[0]]['block'].id, block_graph.nodes[edge_to_add[1]]['block'].id)

def create_json(block_list):
    block_num = len(block_list)
    json_string = '{"type": "FeatureCollection", "features": ['
    for i, block in enumerate(block_list):
        json_string += '\n{"type": "Feature", "geometry":{"type": '
        json_string += f'\"{"Polygon" if isinstance(block.coords, Polygon) else "MultiPolygon"}\", '
        json_string += f'"coordinates":{shapely_to_geojson(block.coords)}'
        json_string += '}, "properties": {'
        json_string += f"\"STATE\" : \"{block.state}\", "
        json_string += f"\"ID\" : \"{block.id}\", "
        json_string += f"\"POP\" : \"{block.pop}\", "
        json_string += f"\"LAND\" : \"{block.land}\", "
        json_string += f"\"WATER\" : \"{block.water}\", "
        json_string += f"\"LONG\" : \"{block.long}\", "
        json_string += f"\"LAT\" : \"{block.lat}\", "
        json_string += f"\"AREA\" : \"{block.area}\", "
        json_string += f"\"DENSITY\" : \"{block.density}\", "

        json_string += f"\"CENTROID\" : \"{block.centroid}\", "
        json_string += f"\"NEIGHBORS\" : \"{block.neighbors}\", "
        # if block.total_votes < block.rep_votes + block.dem_votes:
        #     print("OHHOASDHFOASDFHDOSANO")
        json_string += f"\"TOTAL_VOTES\" : \"{block.total_votes}\", "
        json_string += f"\"REP_VOTES\" : \"{block.rep_votes}\", "
        json_string += f"\"DEM_VOTES\" : \"{block.dem_votes}\", "
        json_string += f"\"WHITE\" : \"{block.white}\", "
        json_string += f"\"BLACK\" : \"{block.black}\", "
        json_string += f"\"HISPANIC\" : \"{block.hispanic}\", "
        json_string += f"\"AAPI\" : \"{block.aapi}\", "
        json_string += f"\"AIAN\" : \"{block.aian}\", "
        json_string += f"\"OTHER\" : \"{block.other}\""
        if i == block_num-1:
            json_string += "}}"
        else:
            json_string += "}},"
        print(f"\rWriting json: {i}/{block_num}, {round(100*i/block_num, 1)}%", end="")
        sys.stdout.flush()
    json_string += "\n]}"
    print("\n", end='')
    return json_string

def create_graph(state_name, check_point="beginning"):

    SOURCE_DIR = "../.." + "/hte-data-new/raw/" + state_name
    if state_name == "california":
        # Do special stuff for california
        pass

    if check_point == "beginning":
        # Load files in to function, and decompress them if necessary
        files = listdir(f"{SOURCE_DIR}")

        if not "block_geodata.json" in files:
            subprocess.run(["7za", "e", f"{SOURCE_DIR}/block_geodata.7z", f"-o{SOURCE_DIR}"])
        with open(f"{SOURCE_DIR}/block_geodata.json", "r") as f:
            block_geodata = json.load(f)
        print("Block geodata loaded.")
        if not "geodata.json" in files:
            subprocess.run(["7za", "e", f"{SOURCE_DIR}/geodata.7z", f"-o{SOURCE_DIR}"])
        with open(f"{SOURCE_DIR}/geodata.json", "r") as f:
            geodata = json.load(f)
        print("Precinct/Block Group geodata loaded.")

        if not "block_demographics.csv" in files:
            subprocess.run(["7za", "e", f"{SOURCE_DIR}/block_demographics.7z",f"-o{SOURCE_DIR}"])
        with open(f"{SOURCE_DIR}/block_demographics.csv", "r") as f:
            block_demographics = pandas.read_csv(f, header=1)
        print("Block Demographics data loaded.")

        with open(f"{SOURCE_DIR}/demographics.csv", "r") as f:
            demographics = pandas.read_csv(f)
        print("Precincts/Block Group Demographics data loaded.")

        with open(f"{SOURCE_DIR}/election_data.csv", "r") as f:
            election_data = pandas.read_csv(f)
        print("Election data loaded.")

        precinct_coordinates = {precinct["properties"]["GEOID10"] :
            precinct["geometry"]["coordinates"] 
            for precinct in geodata["features"]
        }
        block_coordinates = {block["properties"]["GEOID10"] :
            block["geometry"]["coordinates"] 
            for block in block_geodata["features"]
        }
        # print(precinct_coordinates["440010301001"])
        precinct_list = []

        # Precinct/census group ids, pandas Series
        precinct_ids = election_data["GEOID10"] 


        precincts_num = len(precinct_ids)
        precincts_created = 0
        for election_id in precinct_ids:
            rep_votes = election_data[election_data["GEOID10"] == election_id]["Rep_2008_pres"]
            # if rep_votes.size == 2:
            rep_votes = rep_votes.max()
            dem_votes = election_data[election_data["GEOID10"] == election_id]["Dem_2008_pres"]
            dem_votes = dem_votes.max()

            total_votes = election_data[election_data["GEOID10"] == election_id]["Tot_2008_pres"]
            total_votes = total_votes.max()
            if total_votes < rep_votes + dem_votes:
                print("BIG BIG BIG BIG PROBLEM!!!")
            # In addition to total population, racial data needs to be added as well
            total_pop = demographics[demographics["GEOID10"] == election_id]["Tot_2010_tot"].item()
            # print(election_id, "440010301001")
            # print(type(election_id))
            # print(precinct_coordinates["440010301001"])
            try:
                coordinate_data = geojson_to_shapely(precinct_coordinates[election_id])
            except:
                coordinate_data = geojson_to_shapely(precinct_coordinates[str(election_id)])

            precinct = Precinct(total_pop, coordinate_data, state_name, str(election_id), total_votes, rep_votes, dem_votes)
            precinct_list.append(precinct)
            precincts_created += 1
            print(f"\rPrecincts Created: {precincts_created}/{precincts_num}, {round(100*precincts_created/precincts_num, 1)}%", end="")
            sys.stdout.flush()
        print("\n", end="")
        block_ids = block_demographics["id"]
 
        beginning = time.time()
        block_demographics_ids_to_rows = {id : block_demographics.iloc[i] for i, id in enumerate(block_ids)}
        block_geodata_ids_to_properties = {block["properties"]["GEOID10"] : block["properties"] for block in block_geodata["features"]}
        # print(block_demographics_ids_to_rows)
        print(f"Time needed to create: {time.time()-beginning}")
        block_num = len(block_ids)
        block_list = []
        county_to_blocks = {}
        blocks_created = 0
        previous_county = None
        # for i, demographic_id in enumerate(block_ids[107824:]):
        for i, demographic_id in enumerate(block_ids):
            # print(i)
            # begin_time = time.time()
            # row = block_demographics[block_demographics["id"] == demographic_id]
            row = block_demographics_ids_to_rows[demographic_id]
            # print(f"1, {time.time()-begin_time}")
            # print(f"2, {time.time()-begin_time}")
            total_pop = row["Total"].item()
            demographic_id_beginning = demographic_id.find("US")+2
            # print(f"3, {time.time()-begin_time}")
            coordinate_data  = geojson_to_shapely(block_coordinates[demographic_id[demographic_id_beginning:]])
            land = block_geodata_ids_to_properties[demographic_id[demographic_id_beginning:]]["ALAND10"]
            water = block_geodata_ids_to_properties[demographic_id[demographic_id_beginning:]]["AWATER10"]
            lat = block_geodata_ids_to_properties[demographic_id[demographic_id_beginning:]]["INTPTLAT10"]
            long = block_geodata_ids_to_properties[demographic_id[demographic_id_beginning:]]["INTPTLON10"]
            # print(f"4, {time.time()-begin_time}")
            racial_data = {}

            racial_data["hispanic"] = row["Total!!Hispanic or Latino"].item()

            racial_data["white"] = row["Total!!Not Hispanic or Latino!!Population of one race!!White alone"].item()
            racial_data["black"] = row["Total!!Not Hispanic or Latino!!Population of one race!!Black or African American alone"].item()
            racial_data["aian"] = row["Total!!Not Hispanic or Latino!!Population of one race!!American Indian and Alaska Native alone"].item()
            racial_data["asian"] = row["Total!!Not Hispanic or Latino!!Population of one race!!Asian alone"].item()
            racial_data["nhpi"] = row["Total!!Not Hispanic or Latino!!Population of one race!!Native Hawaiian and Other Pacific Islander alone"].item()
            racial_data["other"] = row["Total!!Not Hispanic or Latino!!Population of one race!!Some Other Race alone"].item()
            
            racial_data["white:black"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!White; Black or African American"].item()
            racial_data["white:aian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!White; American Indian and Alaska Native"].item()
            racial_data["white:asian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!White; Asian"].item()
            racial_data["white:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!White; Native Hawaiian and Other Pacific Islander"].item()
            racial_data["white:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!White; Some Other Race"].item()
            racial_data["black:aian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!Black or African American; American Indian and Alaska Native"].item()
            racial_data["black:asian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!Black or African American; Asian"].item()
            racial_data["black:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!Black or African American; Native Hawaiian and Other Pacific Islander"].item()
            racial_data["black:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!Black or African American; Some Other Race"].item()
            racial_data["aian:asian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!American Indian and Alaska Native; Asian"].item() 
            racial_data["aian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["aian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!American Indian and Alaska Native; Some Other Race"].item() 
            racial_data["asian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!Asian; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["asian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!Asian; Some Other Race"].item() 
            racial_data["nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of two races!!Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            
            racial_data["white:black:aian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; Black or African American; American Indian and Alaska Native"].item() 
            racial_data["white:black:asian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; Black or African American; Asian"].item() 
            racial_data["white:black:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; Black or African American; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["white:black:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; Black or African American; Some Other Race"].item() 
            racial_data["white:aian:asian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; American Indian and Alaska Native; Asian"].item() 
            racial_data["white:aian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["white:aian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; American Indian and Alaska Native; Some Other Race"].item() 
            racial_data["white:asian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; Asian; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["white:asian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; Asian; Some Other Race"].item() 
            racial_data["white:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!White; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["black:aian:asian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!Black or African American; American Indian and Alaska Native; Asian"].item() 
            racial_data["black:aian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["black:aian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!Black or African American; American Indian and Alaska Native; Some Other Race"].item() 
            racial_data["black:asian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!Black or African American; Asian; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["black:asian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!Black or African American; Asian; Some Other Race"].item() 
            racial_data["black:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!Black or African American; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["aian:asian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["aian:asian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!American Indian and Alaska Native; Asian; Some Other Race"].item() 
            racial_data["aian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["asian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of three races!!Asian; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            
            racial_data["white:black:aian:asian"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; Black or African American; American Indian and Alaska Native; Asian"].item() 
            racial_data["white:black:aian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["white:black:aian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; Black or African American; American Indian and Alaska Native; Some Other Race"].item() 
            racial_data["white:black:asian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["white:black:asian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; Black or African American; Asian; Some Other Race"].item() 
            racial_data["white:black:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; Black or African American; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["white:aian:asian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["white:aian:asian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; American Indian and Alaska Native; Asian; Some Other Race"].item() 
            racial_data["white:aian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["white:asian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!White; Asian; Native Hawaiian and Other Pacific Islander, Some Other Race"].item() 
            racial_data["black:aian:asian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["black:aian:asian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!Black or African American; American Indian and Alaska Native; Asian; Some Other Race"].item() 
            racial_data["black:aian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["black:asian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["aian:asian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of four races!!American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            
            racial_data["white:black:aian:asian:nhpi"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of five races!!White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander"].item() 
            racial_data["white:black:aian:asian:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of five races!!White; Black or African American; American Indian and Alaska Native; Asian; Some Other Race"].item() 
            racial_data["white:black:aian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of five races!!White; Black or African American; American Indian and Alaska Native; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["white:black:asian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of five races!!White; Black or African American; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["white:aian:asian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of five races!!White; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            racial_data["black:aian:asian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of five races!!Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 

            racial_data["white:black:aian:asian:nhpi:other"] = row["Total!!Not Hispanic or Latino!!Two or More Races!!Population of six races!!White; Black or African American; American Indian and Alaska Native; Asian; Native Hawaiian and Other Pacific Islander; Some Other Race"].item() 
            # print(f"5, {time.time()-begin_time}")
            
            fractional_assignment(racial_data)
            # print(f"6, {time.time()-begin_time}")
            block = Block(total_pop, coordinate_data, state_name, demographic_id, racial_data)
            # print(f"7, {time.time()-begin_time}")
            block.land = float(land)
            block.water = float(water)
            block.long = float(long)
            block.lat = float(lat)
            block.area = block.water + block.land
            block.density = block.pop/block.area
            block.create_racial_data()
            # print(f"8, {time.time()-begin_time}")
            block_list.append(block)
            if previous_county == None or previous_county != demographic_id[demographic_id_beginning:demographic_id_beginning+5]:
                county_to_blocks[demographic_id[demographic_id_beginning:demographic_id_beginning+5]] = [block]
            else:
                county_to_blocks[demographic_id[demographic_id_beginning:demographic_id_beginning+5]].append(block)
            previous_county = demographic_id[demographic_id_beginning:demographic_id_beginning+5]
            # print(previous_county)
            blocks_created += 1
            # print(f"9, {time.time()-begin_time}")
            print(f"\rBlocks Created: {blocks_created}/{block_num}, {round(100*blocks_created/block_num, 1)}%", end="")
            sys.stdout.flush()
        print("\n", end="")
        with open(state_name + "_precinct_list.pickle", "wb") as f:
            pickle.dump(precinct_list, f)
        with open(state_name + "_county_to_block.pickle", "wb") as f:
            pickle.dump(county_to_blocks, f)
        with open(state_name + "_unsplit_block_list.pickle", "wb") as f:
            pickle.dump(block_list, f)
    else:
        with open(state_name + "_precinct_list.pickle", "rb") as f:
            precinct_list = pickle.load(f)
        with open(state_name + "_county_to_block.pickle", "rb") as f:
            county_to_blocks = pickle.load(f)
        with open(state_name + "_unsplit_block_list.pickle", "rb") as f:
            block_list = pickle.load(f)
    # print(time.time()-beginning)
    if check_point != "block_vote_assignment":
        block_num = len(block_list)
        seen_blocks = {}
        # Stores the ids of blocks which are in a precinct {id : [id]}
        precinct_to_blocks = {}
        blocks_matched = 0
        previous_precinct = None
        for precinct in precinct_list:
            possible_blocks = county_to_blocks[precinct.id[:5]]
            accounted_population = 0
            for block in possible_blocks:
                # Temporarily necessary for vermont testing
                # if block.id == "1000000US500239541002044":
                #     continue
                if accounted_population > precinct.pop:
                    break
                if precinct.max_x < block.min_x or precinct.min_x > block.max_x or precinct.max_y < block.min_y or precinct.min_y > block.max_y:
                    continue
                else:
                    if abs(precinct.coords.intersection(block.coords).area-block.coords.area)<0.5*block.coords.area:
                        # print(block.id, precinct.id)
                        if block.id in seen_blocks:
                            print("ALARM BELLS: ", block.id, seen_blocks[block.id], precinct.id)
                        # if precinct.coords.contains(block.coords.exterior.coords):
                        # if precinct.coords.contains(block.coords.representative_point()):
                        # print(previous_precinct, precinct.id)
                        if previous_precinct == None or previous_precinct != precinct.id:
                            precinct_to_blocks[precinct.id] = [block]
                        else:
                            precinct_to_blocks[precinct.id].append(block)
                        previous_precinct = precinct.id
                        accounted_population += block.pop
                        blocks_matched += 1
                        seen_blocks[block.id] = precinct.id
            print(f"\rBlocks Matched: {blocks_matched}/{block_num}, {round(100*blocks_matched/block_num, 1)}%", end="")
            sys.stdout.flush()
        print("\n", end="")
        with open(state_name + "_precinct_to_block.pickle", "wb") as f:
            pickle.dump(precinct_to_blocks, f)
    else:
        with open(state_name + "_precinct_to_block.pickle", "rb") as f:
            precinct_to_blocks = pickle.load(f)

    # When loading from pickles, references for blocks in precinct_to_blocks and block_list are seperate!
    # This needs to be done so that the right blocks are updated with vote counts. 
    ids_to_blocks = {block.id : block for block in block_list}

    for precinct in precinct_list:
        precinct_blocks = precinct_to_blocks[precinct.id]
        # print(precinct_blocks)
        block_pop_sum = sum([block.pop for block in precinct_blocks])
        if block_pop_sum < 0:
            print("NEGATIVE BLOCK AREAS! BIG PROBLEM")
        elif block_pop_sum == 0:
            for block in precinct_blocks:
                ids_to_blocks[block.id].rep_votes = 0
                ids_to_blocks[block.id].dem_votes = 0
                ids_to_blocks[block.id].total_votes = 0
                ids_to_blocks[block.id].other_votes = 0
        else:
            for block in precinct_blocks:
                # try:
                ids_to_blocks[block.id].rep_votes = precinct.rep_votes * block.pop/block_pop_sum
                ids_to_blocks[block.id].dem_votes = precinct.dem_votes * block.pop/block_pop_sum
                ids_to_blocks[block.id].total_votes = precinct.total_votes * block.pop/block_pop_sum
                # except:
                    # print([block.pop for block in precinct_blocks], precinct.id)
            # for block in block_list:
            #     if block.total_votes < block.rep_votes + block.dem_votes:
            #         print("it happens before 537!")
                block.create_election_data()
    # with open("vermont.pickle", "wb") as f:
    #     pickle.dump(block_list, f)
    # with open("vermont.pickle", "rb") as f:
    #     block_list = pickle.load(f)
    del precinct_to_blocks
    del precinct_list

    for block in block_list:
        if block.rep_votes == None and block.dem_votes == None and block.other_votes == None:
            print("it happens before line 544")
    # Split blocks which are not contiguous
    split_multipolygons(block_list)
    # for block in block_list:
    #     if block.total_votes < block.rep_votes + block.dem_votes:
    #         print("it happens before line 546")
    # Combine holes 
    # combine_holypolygons(block_list)
    block_num = len(block_list)
    block_x_sorted = block_list
    block_x_sorted.sort(key=lambda x : x.min_x)
    block_y_sorted = block_list
    block_y_sorted.sort(key=lambda x : x.min_y)

    edges = []
    edges_created = 0
    if block_x_sorted[-1].max_x - block_x_sorted[0].min_x > block_y_sorted[-1].max_y - block_y_sorted[0].min_y:
        del block_y_sorted
        active = [block_x_sorted[0]]
        for i, block in  enumerate(block_x_sorted):
            possible_borders= []
            if i == 0:
                continue
            active_blocks_to_remove = []
            for j, check_block in enumerate(active):
                if check_block.max_x < block.min_x:
                    active_blocks_to_remove.append(j)
                else:
                    possible_borders.append([check_block, block])
            active_blocks_to_remove.sort(reverse=True)
            for index in active_blocks_to_remove:
                active.pop(index)
            active.append(block)
            # print(f"\rBlocks checked: {i}", end="")
            sys.stdout.flush()
            for pairing in possible_borders:
                if pairing[0].max_y < pairing[1].min_y or pairing[1].max_y < pairing[0].min_y:
                    continue
                # if abs(pairing[0].coords.intersection(pairing[1].coords).area - 0) < 0.05*min(pairing[0].coords.area, pairing[1].coords.area):
                intersection = pairing[0].coords.intersection(pairing[1].coords)
                if intersection.is_empty or isinstance(intersection, Point):
                    continue
                if pairing[0].coords.intersection(pairing[1].coords).area == 0 :
                    edges.append(pairing)
                    edges_created += 1
                    print(f"\rEdges Created: {edges_created}, {round(100*i/block_num, 1)}%", end="")
                    sys.stdout.flush()
    else:
        del block_x_sorted
        active = [block_y_sorted[0]]
        for i, block in  enumerate(block_y_sorted):
            possible_borders = []
            if i == 0:
                continue
            active_blocks_to_remove = []
            for j, check_block in enumerate(active):
                if check_block.max_y < block.min_y:
                    active_blocks_to_remove.append(j)
                else:
                    possible_borders.append([check_block, block])
            active_blocks_to_remove.sort(reverse=True)
            for index in active_blocks_to_remove:
                active.pop(index)
            active.append(block)
            # print(f"\rBlocks Checked: {i}/{block_num}, {round(100*i/block_num, 1)}%", end="")
            sys.stdout.flush()
            # print("\n", end="")
            for pairing in possible_borders:
                if pairing[0].max_x < pairing[1].min_x or pairing[1].max_x < pairing[0].min_x:
                    continue
                intersection = pairing[0].coords.intersection(pairing[1].coords)
                if intersection.is_empty or isinstance(intersection, Point):
                    continue
                # if abs(pairing[0].coords.intersection(pairing[1].coords).area - 0) < 0.05*min(pairing[0].coords.area, pairing[1].coords.area):
                if intersection.area == 0:
                    ids = [pairing[0].id, pairing[1].id]
                    if "1000000US500070027013009" in ids and "1000000US500070027013025" in ids:
                        print("wait this still shows up!")
                    edges.append(pairing)
                    edges_created += 1
                    print(f"\rEdges Created: {edges_created}, {round(100*i/block_num, 1)}%", end="")
                    sys.stdout.flush()
    print("\n", end="")
    # for block in block_list:
    #     if block.total_votes < block.rep_votes + block.dem_votes:
    #         print("it happens before line 612")
    print("\n", end="")
    block_graph = nx.Graph()
    for i, block in enumerate(block_list):
        block_graph.add_node(block.id, block=block)
    # node_num = len(block_graph.nodes())
    # print(f"Number of blocks/nodes: {node_num}")
    print("Nodes added to graph")

    edges_num = len(edges)
    for edge in edges:
        block_graph.add_edge(edge[0].id, edge[1].id)
        edge[0].neighbors.append(edge[1].id)
        edge[1].neighbors.append(edge[0].id)
        print(f"\rEdges added to graph: {edges_created}/{edges_num}, {round(100*edges_created/edges_num, 1)}%", end="")
        sys.stdout.flush()
    print("\n")  

    # for block in block_list:
    #     if block.total_votes < block.rep_votes + block.dem_votes:
    #         print("it happens before line 635")
    # with open("vermont_graph.pickle", "rb") as f:
    #     block_graph = pickle.load(f)
    # visualize_graph(
    #     block_graph,
    #     f'./{sys.argv[1]}_no_linking_graph.jpg',
    #     lambda n : block_graph.nodes[n]['block'].centroid,
    #     # sizes=(lambda n : block_graph.nodes[n]['precinct'].pop/500),
    #     show=True
    # )
    connect_islands(block_graph)
    with open(state_name + "_block_list.pickle", "wb") as f:
        pickle.dump(block_list, f)
    json_string = create_json(block_list)
    with open(state_name + "_serialized.json", "w") as f:
        f.write(json_string)
    return block_graph

if __name__ == "__main__":
    try:
        mode = sys.argv[2]
    except:
        block_graph = create_graph(sys.argv[1])
    else:
        if mode not in ["beginning", "block_matching", "block_vote_assignment"]:
            raise Exception("The checkpoint should be one of 'beginning, block_matching, or block_vote_assignment'.")
        else:
            block_graph = create_graph(sys.argv[1], mode)
    print("Serialization Completed. The following time is used for visualizing the graph, which is not essential.")
    # with open(sys.argv[2], "wb+") as f:
    #     pickle.dump(block_graph, f)
    # print(SOURCE_DIR)
    visualize_graph(
        block_graph,
        f'./{sys.argv[1]}_graph.jpg',
        lambda n : block_graph.nodes[n]['block'].centroid,
        # sizes=(lambda n : block_graph.nodes[n]['precinct'].pop/500),
        show=True
    )