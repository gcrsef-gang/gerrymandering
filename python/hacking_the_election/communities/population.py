"""Refines a configuration of political communities in a state so that they all have populations within a certain percent of each other.

Usage:
python3 -m hacking_the_election.communities.population <serialized_state> <n_communities> <max_pop_percentage> (<animation_dir> | "none") <output_path>
"""

import os
import pickle
import random
import sys
import time

from hacking_the_election.communities.initial_configuration import \
    create_initial_configuration
from hacking_the_election.utils.geometry import get_distance
from hacking_the_election.utils.graph import (
    get_giveable_precincts,
    get_takeable_precincts,
    get_components
)
from hacking_the_election.utils.stats import average
from hacking_the_election.visualization.misc import draw_state


def _check_communities_complete(communities, percentage):
    """Checks if communities have satifsfactory populations.

    :param communities: A list of communities.
    :type communities: list of `hacking_the_election.utils.community.Community`

    :param percentage: The maximum tolerated percentage difference between two communities.
    :type percentage: float

    :return: Whether or not the communities fulfil population requirements.
    :rtype: bool
    """

    ideal_pop = average([c.population for c in communities])

    for community in communities:
        if abs(community.population - ideal_pop) / ideal_pop > (percentage / 200):
            return False

    return True


def optimize_population(communities, graph, percentage, animation_dir=None):
    """Takes a set of communities and exchanges precincts so that the population is as evenly distributed as possible.

    :param communities: The current state of the communities within a state.
    :type communities: list of `hacking_the_election.utils.community.Community`

    :param graph: A graph containing precinct data within a state.
    :type graph: `pygraph.classes.graph.graph`

    :param percentage: By how much the populations are able to deviate from one another. A value of 1% means that all the communities must be within 0.5% of the ideal population, so that they are guaranteed to be within 1% of each other.
    :type percentage: float between 0 and 1

    :param animation_dir: Path to the directory where animation files should be saved, defaults to None
    :type animation_dir: str or NoneType
    """

    for community in communities:
        community.update_population()

    if animation_dir is not None:
        draw_state(graph, animation_dir)

    ideal_population = average([c.population for c in communities])
    print(f"{ideal_population=}")

    while not _check_communities_complete(communities, percentage):

        community = max(communities, key=lambda c: abs(c.population - ideal_population))

        if community.population > ideal_population:

            giveable_precincts = get_giveable_precincts(
                graph, communities, community.id)
            
            # Weight random choice by distance from community centroid.
            community_centroid = community.centroid
            giveable_precinct_weights = [
                get_distance(pair[0].centroid, community_centroid)
                for pair in giveable_precincts
            ]
            max_distance = max(giveable_precinct_weights)
            giveable_precinct_weights = \
                [max_distance - weight for weight in giveable_precinct_weights]

            while community.population > ideal_population:
                
                if giveable_precincts == []:
                    giveable_precincts = get_giveable_precincts(
                        graph, communities, community.id)
                    # Weight random choice by distance from community centroid.
                    community_centroid = community.centroid
                    giveable_precinct_weights = [
                        get_distance(pair[0].centroid, community_centroid)
                        for pair in giveable_precincts
                    ]
                    max_distance = max(giveable_precinct_weights)
                    giveable_precinct_weights = \
                        [max_distance - weight for weight in giveable_precinct_weights]

                # Choose random precinct and community and remove from lists.
                precinct, other_community = random.choices(
                    giveable_precincts, weights=giveable_precinct_weights)[0]
                giveable_precinct_weights.pop(
                    giveable_precincts.index((precinct, other_community)))
                giveable_precincts.remove((precinct, other_community))

                community.give_precinct(
                    other_community, precinct.id, update={"population"})
                if len(get_components(community.induced_subgraph)) > 1:
                    # Give back precinct.
                    other_community.give_precinct(
                        community, precinct.id, update={"population"})

        elif community.population < ideal_population:

            takeable_precincts = get_takeable_precincts(
                graph, communities, community.id)
            
            # Weight random choice by distance from community centroid.
            community_centroid = community.centroid
            takeable_precinct_weights = [
                get_distance(pair[0].centroid, community_centroid)
                for pair in takeable_precincts
            ]

            while community.population < ideal_population:

                if takeable_precincts == []:
                    takeable_precincts = get_takeable_precincts(
                        graph, communities, community.id)
                    
                    # Weight random choice by distance from community centroid.
                    community_centroid = community.centroid
                    takeable_precinct_weights = [
                        get_distance(pair[0].centroid, community_centroid)
                        for pair in takeable_precincts
                    ]

                precinct, other_community = random.choices(
                    takeable_precincts, weights=takeable_precinct_weights)[0]
                takeable_precinct_weights.pop(
                    takeable_precincts.index((precinct, other_community)))
                takeable_precincts.remove((precinct, other_community))

                other_community.give_precinct(
                    community, precinct.id, update={"population"})
                if len(get_components(other_community.induced_subgraph)) > 1:
                    # Give back precinct.
                    community.give_precinct(
                        other_community, precinct.id, update={"population"})

        if animation_dir is not None:
            draw_state(graph, animation_dir)

        print([c.population for c in communities], community.population)


if __name__ == "__main__":

    with open(sys.argv[1], "rb") as f:
        graph = pickle.load(f)
    communities = create_initial_configuration(graph, int(sys.argv[2]))

    # TO LOAD INIT CONFIG FROM TEXT FILE:

    # with open("test_vermont_init_config.txt", "r") as f:
    #     precinct_list = eval(f.read())
    # communities = []

    # from hacking_the_election.utils.community import Community

    # for i, community in enumerate(precinct_list):
    #     c = Community(i, graph)
    #     for precinct_id in community:
    #         for node in graph.nodes():
    #             precinct = graph.node_attributes(node)[0]
    #             if precinct.id == precinct_id:
    #                 c.take_precinct(precinct)
    #     communities.append(c)

    animation_dir = None if sys.argv[4] == "none" else sys.argv[4]
    if animation_dir is not None:
        try:
            os.mkdir(animation_dir)
        except FileExistsError:
            pass

    start_time = time.time()
    optimize_population(communities, graph, float(sys.argv[3]), animation_dir)
    print(f"Population optimization took {time.time() - start_time} seconds")

    with open(sys.argv[5], "wb+") as f:
        pickle.dump(communities, f)