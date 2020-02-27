"""
Useful computational geometry functions and classes
for communities algorithm

For interpreting docstrings:
"list" refers to either `list` or `numpy.array`.
"point" refers to a list of two floats that represent a
point in 2-d space.
"segment" refers to a list of two points.
"polygon" refers to a list of segments of which the first represents
the hull of the polygon, and the rest represent any holes in the
polygon.
"shape" refers to an object that can be either a polygon or a
multipolygon (list of polygons).
"""


__all__ = ["clip", "UNION", "DIFFERENCE", "get_if_bordering",
           "get_point_in_polygon", "Community", "group_by_islands",
           "get_precinct_link_pair", "LoopBreakException",
           "LoopContinueException", "get_area_intersection", 
           "shapely_to_polygon", "polygon_to_shapely", "average", "stdev"]


import math
import logging

from shapely.ops import unary_union
from shapely.geometry import MultiLineString, MultiPolygon, Polygon, Point

from .test.utils import print_time


logging.basicConfig(filename="precincts.log", level=logging.DEBUG)


UNION = 1
DIFFERENCE = 2
INTERSECTION = 3


# ===================================================
# custom exceptions


class LoopBreakException(Exception):
    """
    Used to break outer loops from within nested loops.
    """


class LoopContinueException(Exception):
    """
    Used to continue outer loops from within nested loops.
    """


# ===================================================
# general geometry functions


def get_if_bordering(shape1, shape2):
    """
    Returns whether or not two shapes are bordering
    """
    return isinstance(clip([shape1, shape2], INTERSECTION), MultiLineString)


def get_point_in_polygon(polygon, point):
    """
    Returns whether or not point is in polygon
    (with or without holes)

    Polygon can either be list or shapely.geometry.Polygon object
    Point can either be list or shapely.geomtry.Point object

    Returns bool
    """
    if isinstance(polygon, list):
        tuple_polygon = [[tuple(coord) for coord in ring] for ring in polygon]
        shapely_polygon = Polygon(tuple_polygon[0], tuple_polygon[1:])
    elif isinstance(polygon, Polygon):
        shapely_polygon = polygon
    if isinstance(point, list):
        coord = Point(*point)
    elif isinstance(point, Point):
        coord = point
    return shapely_polygon.contains(coord) or shapely_polygon.touches(coord)


def get_area_intersection(polygon1, polygon2):
    """
    Finds the area intersecting between the two polygons passed as arguments
    Both polygons should be shapely polygons
    Returns float (area of intersection.)
    """
    # find area of both polygons
    area1 = polygon1.area
    area2 = polygon2.area
    # find area of union
    union_coords = clip([polygon1, polygon2], 1)
    union_area = union_coords.area
    # The area of the intersection is the sum of the two areas minus the area of the union
    intersect_area = area1 + area2 - union_area
    # if the intersection area is negative, raise exception
    if abs(intersect_area) != intersect_area:
        raise Exception("Negative area found, check inputs")
    return intersect_area

def average(number_list):
    '''
    Finds the average of the integers in number_list.
    Returns float.
    '''
    sum = sum(number_list)
    return sum/len(number_list)

def stdev(number_list, weight_list=None):
    '''
    Finds the standard deviation of the integers in integers list.
    If weight_list applies, multiply each of the numbers in number_list by the weight
    (decimal) corresponding in weight_list. weight_list should have a list of decimals.
    Does not use sample, but all elements in list
    Returns float.
    '''
    average_int = average(number_list)
    squared_sum = 0
    for integer in number_list:
        difference = average_int - integer
        if weight_list:
            squared_sum += (difference * difference) * weight_list
        else:
            squared_sum += (difference * difference)
    return math.sqrt(squared_sum / len(number_list))

def clip(shapes, clip_type):
    """
    Finds external border of a group of shapes

    Args:
    `shapes`: array of array of array of vertices
    `clip_type`: either 1 (union) or 2 (difference)

    if `clip_type` is difference, then there should only be 2 shapes in
    `shapes`

    Returns array of vertices
    """
    if clip_type == 1:
        solution = unary_union(shapes)
    else:
        if len(shapes) != 2:
            raise ValueError(
                "Polygon clip of type DIFFERENCE takes exactly 2 input shapes"
                )
        if clip_type == 2:    
            solution = shapes[0].difference(shapes[1])
        elif clip_type == 3:
            solution = shapes[0].intersection(shapes[1])
        else:
            raise ValueError(
                "Invalid clip type. Use utils.UNION or utils.DIFFERENCE")
    return solution

def polygon_to_shapely(polygon):
    """
    Converts list-type polygon `shape` to
    `shapely.geometry.Polygon`
    """
    tuple_polygon = [[tuple(coord) for coord in linear_ring]
                     for linear_ring in polygon]
    return Polygon(tuple_polygon[0], tuple_polygon[1:])

def shapely_to_polygon(polygon):
    """
    Creates json polygon from shapely.geometry.Polygon
    NOTE: Assumes shapely polygon only has exterior and no holes.
    """
    coordinates = list(polygon.exterior.coords)
    linear_ring = []
    for tuple1 in coordinates:
        x = tuple1[0]
        y = tuple1[1]
        point_list = [x, y]
        linear_ring.append(point_list)
    return [linear_ring]
# ===================================================
# Community algorithm-specifc functions and classes:


class Community:
    """
    A collection of precincts
    """
    
    def __init__(self, precincts, identifier):
        self.precincts = {precinct.vote_id: precinct for precinct in precincts}
        self.id = identifier
        if precincts != []:
            self.coords = clip([p.coords for p in self.precincts.values()], UNION)
        else:
            self.coords = Polygon()
        self.partisanship = None
        self.standard_deviation = None
        self.population = None
        self.compactness = None

    def update_compactness(self):
        """
        Updates the `compactness` attribute.

        Implemenatation of this algorithm (schwartzberg):
        https://fisherzachary.github.io/public/r-output.html
        """
        area = self.coords.area
        circumference = 2 * math.pi * math.sqrt(area / math.pi)
        perimeter = self.coords.length
        self.compactness = circumference / perimeter

    def update_standard_deviation(self):
        """
        Updates the `standard_deviation` attribute.
        """

        try:
            rep_percentages = [
                p.r_election_sum / (p.r_election_sum + p.d_election_sum) * 100
                for p in self.precincts]
            mean = sum(rep_percentages) / len(rep_percentages)
            
            self.standard_deviation = math.sqrt(sum([(p - mean) ** 2 for p in rep_percentages]))
        except ZeroDivisionError:
            self.standard_deviation = 0.0

    def update_partisanship(self):
        """
        Updates the `partisanship` attribute
        """

        rep_sum = 0
        total_sum = 0
        for precinct in self.precincts:
            if (r_sum := precinct.r_election_sum) != -1:
                rep_sum += r_sum
                total_sum += r_sum + precinct.d_election_sum
        self.partisanship = rep_sum / total_sum

    def give_precinct(self, other, precinct_id, coords=True,
                      partisanship=True, standard_deviation=True,
                      population=True, compactness=True):
        """
        Gives precinct from self to other community.

        All parameters with default value of `True` indicate whether or
        not to update that attribute after the community is given.
        """

        if not isinstance(other, Community):
            raise TypeError(f"Invalid type {type(other)}.\n"
                            "Can only give precinct to community.")
        try:
            precinct = self.precincts[precinct_id]
        except KeyError:
            raise ValueError(
                f"No precinct in community with id '{precinct_id}.'")

        del self.precincts[precinct_id]
        other.precincts[precinct_id] = precinct
        # Update borders
        if coords:
            self.coords = clip([self.coords, precinct.coords],
                               DIFFERENCE)
            other.coords = clip([p.coords for p in other.precincts.values()],
                                UNION)

        # Update other attributes that are dependent on precincts attribute
        for community in [self, other]:
            if partisanship:
                community.partisanship = Community.get_partisanship(
                    community.precincts.values())
            if standard_deviation:
                community.standard_deviation = \
                    Community.get_standard_deviation(
                        community.precincts.values())
            if population:
                community.population = sum(
                    [precinct.population for precinct in
                     community.precincts.values()])
            if compactness:
                community.compactness = get_schwartzberg_compactness(
                    community.coords)

    def get_bordering_precincts(self, unchosen_precincts):
        """
        Returns list of precincts bordering `self`

        `unchosen_precincts` is a Community object that contains all
        the precincts in the state that haven't already been added to
        a community
        """
        bordering_precincts = set()
        if self.precincts != {}:
            for vote_id, precinct in unchosen_precincts.precincts.items():
                if get_if_bordering(precinct.coords, self.coords):
                    bordering_precincts.add(precinct.vote_id)
        else:
            bordering_precincts = set(unchosen_precincts.precincts.keys())
        return bordering_precincts


def group_by_islands(precincts):
    """
    Returns list of precincts sorted into
    lists by what island they are on.
    """
    state_border = clip([p.coords for p in precincts], UNION)

    if isinstance(state_border, MultiPolygon):
        # There are islands in the state.

        island_polygons = state_border.geoms
        islands = [[] for _ in range(len(island_polygons))]

        for precinct in precincts:
            for i, island in enumerate(island_polygons):
                # If the first point of the precinct is in this island,
                # all of them must be.
                if get_point_in_polygon(
                        island, list(precinct.coords.exterior.coords[1])):
                    islands[i].append(precinct.vote_id)
        return islands
    else:
        return [[p.vote_id for p in precincts]]


def get_precinct_link_pair(island, island_precinct_groups):
    """
    Finds id of precinct that is closest to
    `precinct` on any other island.

    Args:
        `island`:                 List of `save_precincts.Precinct`
                                  objects that is create the island
                                  you want to find the precinct that
                                  is closest to.
        `island_precinct_groups`: List of lists of
                                  `save_precincts.Precinct` objects
                                  grouped by islands in the whole state
                                  minus `island`.

    Returns list of two strings that are the linked
    pair between `island` and any other island.
    """
    island_borders = [clip([p.coords for p in island], UNION)
                      for island in island_precinct_groups]
    # List of precincts that border the "coastline" of the each island.
    # Grouped by island.
    border_precincts = \
        [[p for p in island if get_if_bordering(p.coords, island_border)]
         for p in island for island in island_borders]

    island_centroid = \
        clip([p.coords for p in island], UNION).centroid.coords[0]
    # id of Precinct whose centroid is closest to centroid of `island`
    closest_precinct = None
    # Distance from above precinct to centroid of `island`
    closest_precinct_distance = 0
    # Island that contains above precinct
    closest_isalnd = []
    for i in range(len(border_precincts)):
        for precinct in border_precincts[i]:
            distance = _get_distance(island_centroid,
                                     precinct.centroid.coords[0])
            if (
                    closest_precinct is None
                    or distance < closest_precinct_distance
                    ):
                closest_precinct = precinct.vote_id
                closest_precinct_distance = distance
                closest_island = i
    closest_island_centroid = \
        island_borders[closest_island].centroid.coords[0]

    # Find the precinct on the border of `island` that is closest to
    # the centroid of the island that contains the precincts that is
    # closest to the centroid of `island`.
    island_border_precincts = [precinct for precinct in islands
                               if get_if_bordering(p.coords, island_border)]
    closest_second_precinct = None
    closest_second_precinct_distance = 0
    for precinct in island_border_precincts:
        distance = _get_distance(closest_island_centroid,
                                 precinct.centroid.coords[0])
        if (
                closest_second_precinct is None
                or distance < closest_second_precinct_distance
                ):
            closest_second_precinct = precinct.vote_id
            closest_precinct_distance = distance
    return [closest_precinct, closest_second_precinct]
