import unittest
from unittest.mock import patch
from simulation.model import CommunicationNetwork, TimeVaryingHypergraph
import os

class TimeVaryingHypergraphTest(unittest.TestCase):
    cn = TimeVaryingHypergraph(
        {"h1": ["v1", "v2"], "h2": ["v2", "v3"], "h3": ["v3", "v4"]},
        {"h1": 1, "h2": 2, "h3": 3},
    )

    # Testing if the timings function works as expected when given no input
    def test_timings_no_parameter(self):
        self.assertEqual(len(self.cn.timings()), 3)

    # Testing if the timings function works as expected when given correct input
    def test_timings_correct_parameter(self):
        self.assertEqual(self.cn.timings("h1"), 1)

    # Testing if the timings function works as expected when given incorrect input
    def test_timings_incorrect_paramter(self):
        with self.assertRaises(Exception) as context:
            self.cn.timings("x1")
        self.assertTrue("No hyperedge matches the timing x1" in str(context.exception))

    # Testing if the vertices function works as expected when given no input
    def test_vertices_no_parameter(self):
        self.assertEqual(len(self.cn.vertices()), 4)

    # Testing if the vertices function works as expected when given correct input
    def test_vertices_correct_parameter(self):
        self.assertEqual(self.cn.vertices("h1"), {"v1", "v2"})

    # Testing if the vertices function works as expected when given incorrect input
    def test_vertices_incorrect_parameter(self):
        with self.assertRaises(Exception) as context:
            self.cn.vertices("x1")
        self.assertTrue("Unknown hyperedge x1" in str(context.exception))

    # Testing if the hyperedges function works as expected when given no input
    def test_hyperedges_no_parameter(self):
        self.assertEqual(len(self.cn.hyperedges()), 3)

    # Testing if the hyperedges function works as expected when given correct input
    def test_hyperedges_correct_parameter(self):
        self.assertEqual(self.cn.hyperedges("v1"), {"h1"})

    # Testing if the hyperedges function works as expected when given incorrect input
    def test_hyperedges_incorrect_parameter(self):
        with self.assertRaises(Exception) as context:
            self.cn.hyperedges("x1")
        self.assertTrue("Unknown vertex x1" in str(context.exception))

class CommunicationNetworkTest(unittest.TestCase):
    def setUp(self):
        try:
            import orjson
            self.json = "orjson.loads"
        except:
            self.json = "json.loads"

        self.dummy_file = "test/testfile.json"
        with open(self.dummy_file, "w") as f:
            f.write("")
        
    def tearDown(self):
        os.remove(self.dummy_file)

    # Testing if the from_json function works as expected when the list for participants is empty
    def test_from_json_empty_participants(self):
        # Mock the file reading and decompression
        data = {"1": {"end": "2020-02-05T12:49:39", "participants": [0.1]},
                    "2": {"end": "2020-02-05T12:49:39", "participants": [2, 3]},
                    "3": {"end": "2020-02-05T12:49:39", "participants": ["2"]},
                    "4": {"end": "2020-02-05T12:49:59", "participants": []},
                    "5.3": {"end": "2020-02-05T12:49:59", "participants": [3, 7]}
                }
                
        # Patch the required functions and objects with the mocks
        with patch(self.json, return_value=data) as _:

            # Create an object with a call to the method to be tested to make sure we get the error we want
            with self.assertRaises(SystemExit) as context:
                CommunicationNetwork.from_json(self.dummy_file)
            
            self.assertEqual("Line: 3, Chan_id: 4. Participants column empty.", str(context.exception))

    # Testing if the from_json function works as expected when the value for datetime is incorrect
    def test_from_json_wrong_datetime(self):
        # Mock the file reading and decompression
        data = {"1": {"end": "2020-02-05T12:49:39", "participants": [0.1]},
                    "2": {"end": "2020-02-05T12:49:39", "participants": [2, 3]},
                    "3": {"end": "hejsan", "participants": ["2"]},
                    "4": {"end": "2020-02-05T12:49:59", "participants": [3]},
                    "5.3": {"end": "2020-02-05T12:49:59", "participants": [3, 7]}
                }

        # Patch the required functions and objects with the mocks
        with patch(self.json, return_value=data) as _:

            # Create an object with a call to the method to be tested to make sure we get the error we want
            with self.assertRaises(SystemExit) as context:
                CommunicationNetwork.from_json(self.dummy_file)

            self.assertEqual("Line: 2, Chan_id: 3. End column not compatible datetime format.", str(context.exception))

class CommunicationNetworkTestIntegration(unittest.TestCase):
    def setUp(self):
        try:
            import orjson
            self.json = "orjson.loads"
        except:
            self.json = "json.loads"

        self.dummy_file_uncompressed = "test/testfile.json"
        with open(self.dummy_file_uncompressed, "w") as f:
            f.write("")

        self.dummy_file_compressed = "test/testfile.bz2"
        with open(self.dummy_file_compressed, "w") as f:
            f.write("")
            
        self.data = {
                "00": {"end": "2020-02-05T12:49:39", "participants": [0, 1]},
                "01": {"end": "2020-02-05T12:49:49", "participants": [2, 3]},
                "02": {"end": "2020-02-05T12:49:59", "participants": [4, 5]},
                "03": {"end": "2020-02-05T12:49:19", "participants": [6]},
                "04": {"end": "2020-02-05T12:49:29", "participants": [7, 8, 9]},
                "05": {"end": "2020-02-05T12:59:39", "participants": [1, 4]},
                "06": {"end": "2020-02-05T12:59:30", "participants": [2, 7]},
                "07": {"end": "2020-02-05T12:59:39", "participants": [5, 2]},
                "08": {"end": "2020-02-05T12:49:31", "participants": [3]},
                "09": {"end": "2020-02-05T12:49:32", "participants": [8, 11]},
                "10": {"end": "2020-02-05T12:49:33", "participants": [0, 9]},
                "11": {"end": "2020-02-05T12:49:34", "participants": [5, 6]},
                "12": {"end": "2020-02-05T12:49:35", "participants": [9, 8]}
            }
        
    def tearDown(self):
        os.remove(self.dummy_file_compressed)
        os.remove(self.dummy_file_uncompressed)

    # Testing if the from_json function works as expected when the values are compressed and correct
    def test_from_json_compressed_integration(self):
        # Patch the required functions and objects with the mocks
        with patch(self.json, return_value=self.data)as _:

            # Create an object with a call to the method to be tested to make sure the mock is read
            result = CommunicationNetwork.from_json(self.dummy_file_compressed)

            # Assert that the object was created with the default name
            self.assertEqual(result.name, None)

            # Assert that the inherited functions work as expected
            self.assertSetEqual(result.channels(), {'00', '01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12'})
            self.assertSetEqual(result.channels(0), {'00', '10'})
            self.assertSetEqual(result.channels(5), {'02', '07', '11'})
            self.assertSetEqual(result.channels(9), {'04', '10', '12'})

            # Assert that the inherited functions work as expected
            self.assertSetEqual(result.participants(), {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11})
            self.assertSetEqual(result.participants("00"), {0, 1})
            self.assertSetEqual(result.participants("04"), {7, 8, 9})
            self.assertSetEqual(result.participants("08"), {3})

    # Testing if the from_json function works as expected when the values are uncompressed and correct
    def test_from_json_uncompressed_integration(self):
        # Patch the required functions and objects with the mocks
        with patch(self.json, return_value=self.data) as _:

            # Create an object with a call to the method to be tested to make sure the mock is read
            result = CommunicationNetwork.from_json(self.dummy_file_uncompressed)

            # Assert that the object was created with the default name
            self.assertEqual(result.name, None)

            # Assert that the inherited functions work as expected
            self.assertSetEqual(result.channels(), {'00', '01', '02', '03', '04', '05', '06', '07', '08', '09','10', '11', '12'})
            self.assertSetEqual(result.channels(0), {'00', '10'})
            self.assertSetEqual(result.channels(5), {'02', '07', '11'})
            self.assertSetEqual(result.channels(9), {'04', '10', '12'})

            # Assert that the inherited functions work as expected
            self.assertSetEqual(result.participants(), {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11})
            self.assertSetEqual(result.participants("00"), {0, 1})
            self.assertSetEqual(result.participants("04"), {7, 8, 9})
            self.assertSetEqual(result.participants("08"), {3})

