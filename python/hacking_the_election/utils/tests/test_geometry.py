"""Unit tests for `hacking_the_election.utils.geometry`
"""


import json
import math
import os
import pickle
import sys
import unittest

from shapely.geometry import MultiPolygon, Point

from hacking_the_election.utils import community, geometry, precinct
from hacking_the_election.visualization.map_visualization import visualize_map


SOURCE_DIR = os.path.dirname(__file__)
SHOW = False


# Load data files.
with open(f"{SOURCE_DIR}/data/geometry/original_gerrymander.json", "r") as f:
    # Stored as GeoJson, not shapely object.
    ORIGINAL_GERRYMANDER = \
        json.load(f)["features"][0]["geometry"]["coordinates"]

with open(f"{SOURCE_DIR}/data/geometry/vermont_precincts.json", "r") as f:
    vermont_precincts_json = json.load(f)

# Dict linking geoid10 to shapely object containing coordinates.
VERMONT_PRECINCTS = {}
for p in vermont_precincts_json["features"]:
    VERMONT_PRECINCTS[p["properties"]["GEOID10"]] = \
        geometry.geojson_to_shapely(p["geometry"]["coordinates"])

with open(f"{SOURCE_DIR}/data/geometry/vermont.json", "r") as f:
    # Total state boundary of Vermont.
    VERMONT = geometry.geojson_to_shapely(
        json.load(f)["features"][0]["geometry"]["coordinates"])

with open(f"{SOURCE_DIR}/data/vermont_graph.pickle", "rb") as f:
    VERMONT_GRAPH = pickle.load(f)


class TestGeometry(unittest.TestCase):

    def test_geojson_to_shapely(self):
        """Tests `hacking_the_election.utils.geometry.geojson_to_shapely`
        
        If SHOW is True, then:
        Working under assumption that visualization functions are working.
        Purely for human observation.

        Otherwise simply checks that the function does not throw an error.
        """

        original_gerrymander_polygon = geometry.geojson_to_shapely(ORIGINAL_GERRYMANDER)

        if SHOW:
            visualize_map([original_gerrymander_polygon], None, show=True)

    def test_shapely_to_geojson(self):
        """Tests `hacking_the_election.utils.geometry.geojson_to_shapely`

        Checks that the function does not throw an error.
        """

        polygons = [
            Point(0, 0).buffer(50),
            Point(100, 100).buffer(10)
        ]

        geometry.shapely_to_geojson(polygons[0])
        geometry.shapely_to_geojson(MultiPolygon(polygons))

    def test_get_if_bordering(self):
        """Tests `hacking_the_election.utils.geometry.get_if_bordering`

        Tests various precinct borders that were previously not working properly with function.
        All within state of vermont.
        """
        self.assertEqual(
            geometry.get_if_bordering(
                VERMONT_PRECINCTS["50009VD85"],
                VERMONT_PRECINCTS["50009VD77"]
            ),
            True
        )
        self.assertEqual(
            geometry.get_if_bordering(
                VERMONT_PRECINCTS["50003VD37"],
                VERMONT_PRECINCTS["50009VD77"]
            ),
            False
        )
        self.assertEqual(
            geometry.get_if_bordering(
                VERMONT,
                VERMONT_PRECINCTS["50009VD85"],
                inside=True
            ),
            True
        )

    def test_get_compactness(self):
        """Tests `hacking_the_election.utils.geometry.get_compactness`
        """

        original_gerrymander_polygon = \
            geometry.geojson_to_shapely(ORIGINAL_GERRYMANDER)

        original_reock_score = round(geometry.get_compactness(original_gerrymander_polygon), 3)
        self.assertEqual(original_reock_score, 0.32)

        vermont_reock_score = round(geometry.get_compactness(VERMONT), 3)
        self.assertEqual(vermont_reock_score, 0.423)

    def test_area(self):
        """Tests `hacking_the_election.utils.geometry.area`
        """

        precinct = VERMONT_PRECINCTS["50009VD85"]

        precinct_area = round(
            geometry.area(geometry.shapely_to_geojson(precinct)[0]), 3)

        self.assertEqual(
            precinct_area,
            round(VERMONT_PRECINCTS["50009VD85"].area, 3)
        )

    def test_get_distance(self):
        """Tests `hacking_the_election.utils.geometry.get_distance`
        """
        self.assertEqual(
            geometry.get_distance([0, 0], [4, 4]),
            32
        )

    def test_get_imprecise_compactness(self):
        """Tests `hacking_the_election.utils.geometry.get_imprecise_compactness`
        """

        # Create circle-shaped community.

        circle = Point(0, 0).buffer(10)

        n_precincts = len(list(circle.exterior.coords))

        precincts = []
        for i, point in enumerate(list(circle.exterior.coords)):
            precinct_coords = Point(*point).buffer(math.sqrt((100 * math.pi / n_precincts) / math.pi))
            p = precinct.Precinct(0, precinct_coords, "vermont", str(i), 0, 0)
            p.node = i
            precincts.append(p)

        c = community.Community(0, VERMONT_GRAPH)
        for p in precincts:
            c.take_precinct(p)

        # Compactness of a circle should equal 1.
        self.assertLess(abs(geometry.get_imprecise_compactness(c) - 1), 0.1)


if __name__ == "__main__":
    if "-s" in sys.argv[1:]:
        SHOW = True
        sys.argv.remove("-s")

    unittest.main()