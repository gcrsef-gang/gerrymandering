"""
Refines a state broken into communities
so that they are compact within a threshold.
"""

import math
import pickle
import random
import warnings

from shapely.geometry import Point
import matplotlib.pyplot as plt

from hacking_the_election.test.funcs import (
    polygon_to_list,
    convert_to_json
)
from hacking_the_election.utils.compactness import (
    add_precinct,
    format_float,
    get_average_compactness
)
from hacking_the_election.utils.exceptions import (
    CreatesMultiPolygonException,
    ExitException,
    LoopBreakException,
    ZeroPrecinctCommunityException
)
from hacking_the_election.utils.geometry import (
    clip,
    DIFFERENCE,
    get_if_bordering,
    INTERSECTION
)


def signal_handler(sig, frame):
    raise ExitException


def refine_for_compactness(communities, minimum_compactness,
                           linked_precincts, output_json, output_pickle):
    """
    Returns communities that are all below the minimum compactness.
    """

    precincts = {p for c in communities for p in c.precincts.values()}
    for community in communities:
        community.update_compactness()

    try:
        X = [[] for _ in communities]
        Y = [[] for _ in communities]
        i = 0

        while True:
            try:
                print("Average community compactness: "
                        f"{get_average_compactness(communities)}")

                # Find circle with same area as district.
                radius = math.sqrt(community.coords.area / math.pi)
                center = community.coords.centroid.coords[0]
                circle = Point(*center).buffer(radius)

                # Find precincts that need to be added to this community.
                inside_circle = set()
                bordering_communities = \
                    [c for c in communities
                     if get_if_bordering(c.coords, community.coords)
                        and c != community]
                for precinct in [p for c in bordering_communities
                                 for p in c.precincts.values()]:
                    if precinct not in linked_precincts:
                        if get_if_bordering(precinct.coords,
                                            community.coords):
                            # Section of precinct that is inside of circle.
                            circle_intersection = \
                                clip([circle, precinct.coords], INTERSECTION)
                            # If precinct and circle are intersecting
                            if not circle_intersection.is_empty:
                                intersection_area = circle_intersection.area
                                precinct_area = precinct.coords.area
                                if intersection_area > (precinct_area / 2):
                                    inside_circle.add(precinct)
                
                # Find precincts that need to be removed from this community.
                outside_circle = set()

                outside_bordering_precincts = community.get_outside_precincts()
                for precinct in outside_bordering_precincts:
                    if precinct not in linked_precincts:
                        # Section of precinct that is outside of circle.
                        circle_difference = clip([precinct.coords, circle],
                                                    DIFFERENCE)
                        # If precinct is not entirely in circle
                        if not circle_difference.is_empty:
                            difference_area = circle_difference.area
                            precinct_area = precinct.coords.area
                            if difference_area > (precinct_area / 2):
                                outside_circle.add(precinct)

                while outside_circle != set() or inside_circle != set():
                    # Add precincts one by one
                    try:
                        precinct = random.sample(outside_circle, 1)[0]
                        try:
                            try:
                                add_precinct(
                                    communities, community, precinct, True)
                                print(f"Removed {precinct.vote_id} from "
                                      f"community {community.id}. Compactness: "
                                      f"{round(community.compactness, 3)}")
                            except (CreatesMultiPolygonException,
                                    ZeroPrecinctCommunityException):
                                pass
                        except IndexError:
                            # Precinct was outside of circle but not
                            # bordering any other community.
                            pass
                        outside_circle.discard(precinct)
                    except ValueError:
                        # No precincts left in `outside_circle`
                        precinct = random.sample(inside_circle, 1)[0]
                        try:
                            try:
                                add_precinct(
                                    communities, community, precinct, False)
                                print(f"Added {precinct.vote_id} to community "
                                      f"{community.id}. Compactness: "
                                      f"{round(community.compactness, 3)}")
                            except (CreatesMultiPolygonException,
                                    ZeroPrecinctCommunityException):
                                pass
                        except ValueError as e:
                            warnings.warn(str(e))
                        inside_circle.discard(precinct)

                    if all([c.compactness > minimum_compactness
                            for c in communities]):

                        print([c.compactness for c in communities])
                        i += 1
                        for x, c in enumerate(communities):
                            Y[x].append(c.compactness)
                            X[x].append(i)
                        raise LoopBreakException
                    if community.compactness > minimum_compactness:
                        i += 1
                        for x, c in enumerate(communities):
                            Y[x].append(c.compactness)
                            X[x].append(i)
                        print(f"Community {community.id} has "
                               "compactness above threshold.")
                        break

                if community.compactness <= minimum_compactness:
                    i += 1
                    for x, c in enumerate(communities):
                        Y[x].append(c.compactness)
                        X[x].append(i)
                    print(f"Community {community.id} failed to get above "
                            "threshold after adding and removing all "
                            "precincts in and out of circle.")

                community = \
                    random.choice([c for c in communities if c != community])
                
            except LoopBreakException:
                break
    finally:
        with open(output_pickle, "wb+") as f:
            pickle.dump(communities, f)
        convert_to_json(
            [polygon_to_list(c.coords) for c in communities],
            output_json,
            [{"ID": c.id} for c in communities]
        )
        for x, y in zip(X, Y):
            plt.plot(x, y)
        plt.show()
        with open("test_compactness_graph.pickle", "wb+") as f:
            pickle.dump([X, Y], f)


if __name__ == "__main__":

    import signal
    import sys

    from hacking_the_election.utils.community import Community
    from hacking_the_election.serialization import save_precincts


    sys.modules["save_precincts"] = save_precincts

    signal.signal(signal.SIGINT, signal_handler)

    with open(sys.argv[1], "rb") as f:
        communities, linked_precinct_chains = pickle.load(f)
    linked_precincts = {p for chain in linked_precinct_chains for p in chain}

    refine_for_compactness(communities, float(sys.argv[2]),
                           linked_precincts, sys.argv[3], sys.argv[4])