"""
Unit tests for utils.py
"""

import sys
from os.path import abspath, dirname
import unittest
import time
import pickle

import numpy as np
import matplotlib.pyplot as plt

sys.path.append(abspath(dirname(dirname(dirname(__file__)))))

from utils import convert_to_json
from serialization.load_precincts import load
from serialization.save_precincts import Precinct
from gerrymandering.utils import (get_equation, get_segments, clip, UNION,
                                  DIFFERENCE)


def print_time(func):
    def timed_func(*args, **kwargs):
        start_time = time.time()
        output = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start_time} seconds")
        return output
    return timed_func


def return_time(func):
    def timed_func(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        return time.time() - start_time
    return timed_func


class TestUtils(unittest.TestCase):

    # complete pickle state data files
    # ================================

    # for small tests that shouldnt take long
    vermont = load(dirname(__file__) + "/data/vermont.pickle")
    # for big tests to find problems
    alabama = load(dirname(__file__) + "/data/alabama.pickle")
    # for things with islands
    hawaii = load(dirname(__file__) + "/data/hawaii.pickle")
    # for small tests that need more than one district
    connecticut = load(dirname(__file__) + "/data/connecticut.pickle")

    # function-specific test data
    # ================================
    
    difference_test_data = load(dirname(__file__) \
                                + "/data/difference_test_data.pickle")
    border_test_data = load(dirname(__file__) \
                                + "/data/border_test_data.pickle")


    @classmethod
    def plot_get_border(cls):
        """
        Creates scatter plot of all relationship between number of
        precincts and time
        """

        timed_get_border = lambda shapes: return_time(clip)(shapes, UNION)

        X = np.arange(1, len(cls.vermont[0]) + 1)
        Y = np.array([])
        for i in range(1, len(cls.vermont[0]) + 1):
            t = timed_get_border([p.coords for p in cls.vermont[0][:i]])
            Y = np.append(Y, [t])

        # save the data in case the chart doesn't work
        with open("test_border_time.pickle", "wb+") as f:
            pickle.dump(Y, f)
        
        plt.scatter(X, Y)
        plt.show()

    def __init__(self, *args, **kwargs):

        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_get_equation(self):
        
        seg1 = np.array([[3, 1], [7, 0]])
        seg2 = np.array([[0, 0], [0, 0]])
        seg3 = np.array([])

        self.assertEqual(-748.25, get_equation(seg1)(3000))
        with self.assertRaises(ValueError):
            get_equation(seg2)
        with self.assertRaises(ValueError):
            get_equation(seg3)


    def test_get_segments(self):

        # normal polygon
        shape_1 = np.array([[0, 0], [2, 0], [2, 2], [0, 2]])
        # vermont polygon
        shape_2 = np.array(self.vermont[0][0].coords)

    def test_get_border(self):
        """
        Border of precincts of vermont
        """

        @print_time
        def test_get_border_speed():
            return clip([p.coords for p in self.vermont[0]], UNION)

        self.assertEqual(test_get_border_speed(), self.border_test_data)

    def test_get_difference(self):
        """
        Difference between outer border of connecticut and
        its 5th congressional district
        """

        @print_time
        def test_get_difference_speed():
            connecticut_district_coords = [
                d["geometry"]["coordinates"]
                for d in self.connecticut[1]["features"]]

            outer_border = clip(connecticut_district_coords, UNION)
            difference = clip([outer_border, connecticut_district_coords[4]],
                              DIFFERENCE)

            return difference

        self.assertEqual(test_get_difference_speed(), self.difference_test_data)


    def test_get_schwartsberg_compactness(self):
        pass

    def test_get_if_addable(self):
        pass

    def test_community(self):
        """
        To test Community class
        """
        pass


if __name__ == "__main__":
    if "border_graph" in sys.argv:
        TestUtils.plot_get_border()
    else:
        unittest.main()

