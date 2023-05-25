import unittest
from unittest.mock import patch
from simulation.model import CommunicationNetwork, TimeVaryingHypergraph
import os


class TestTimeVaryingHypergraph(unittest.TestCase):
    """
    A test case for the TimeVaryingHypergraph class.
    """

    graph = TimeVaryingHypergraph(
        {"h1": ["v1", "v2"], "h2": ["v2", "v3"], "h3": ["v3", "v4"]},
        {"h1": 1, "h2": 2, "h3": 3},
    )

    def test_timings_no_parameter(self):
        """
        Testing if the timings function works as expected when given no input
        """
        self.assertEqual(len(self.graph.timings()), 3)

    def test_timings_correct_parameter(self):
        """
        Testing if the timings function works as expected when given correct input
        """
        self.assertEqual(self.graph.timings("h1"), 1)

    def test_timings_incorrect_paramter(self):
        """
        Testing if the timings function works as expected when given incorrect input
        """
        with self.assertRaises(Exception) as context:
            self.graph.timings("x1")
        self.assertTrue("No hyperedge matches the timing x1" in str(context.exception))

    def test_vertices_no_parameter(self):
        """
        Testing if the vertices function works as expected when given no input
        """
        self.assertEqual(len(self.graph.vertices()), 4)

    def test_vertices_correct_parameter(self):
        """
        Testing if the vertices function works as expected when given correct input
        """
        self.assertEqual(self.graph.vertices("h1"), {"v1", "v2"})

    def test_vertices_incorrect_parameter(self):
        """
        Testing if the vertices function works as expected when given incorrect input

        """
        with self.assertRaises(Exception) as context:
            self.graph.vertices("x1")
        self.assertTrue("Unknown hyperedge x1" in str(context.exception))

    def test_hyperedges_no_parameter(self):
        """
        Testing if the hyperedges function works as expected when given no input
        """
        self.assertEqual(len(self.graph.hyperedges()), 3)

    def test_hyperedges_correct_parameter(self):
        """
        Testing if the hyperedges function works as expected when given correct input

        """
        self.assertEqual(self.graph.hyperedges("v1"), {"h1"})

    def test_hyperedges_incorrect_parameter(self):
        """
        Testing if the hyperedges function works as expected when given incorrect input
        """
        with self.assertRaises(Exception) as context:
            self.graph.hyperedges("x1")
        self.assertTrue("Unknown vertex x1" in str(context.exception))


class TestCommunicationNetwork(unittest.TestCase):
    """
    A test case for the CommunicationNetwork class.
    """

    def setUp(self):
        """
        Differentiating between normal json and orjson depending on which is installed and creating a dummy file
        """
        try:
            import orjson

            self.json_function_used = "orjson.loads"
        except:
            self.json_function_used = "json.loads"

        self.dummy_file = "test/testfile.json"
        with open(self.dummy_file, "w") as f:
            f.write("")

    def tearDown(self):
        """
        Removing the file created in the setup
        """
        os.remove(self.dummy_file)

    def test_from_json_empty_participants(self):
        """
        Testing if the from_json function works as expected when the list for participants is empty
        """
        data = {
            "1": {"end": "2020-02-05T12:49:39", "participants": [0.1]},
            "2": {"end": "2020-02-05T12:49:39", "participants": [2, 3]},
            "3": {"end": "2020-02-05T12:49:39", "participants": ["2"]},
            "4": {"end": "2020-02-05T12:49:59", "participants": []},
            "5.3": {"end": "2020-02-05T12:49:59", "participants": [3, 7]},
        }

        with patch(self.json_function_used, return_value=data) as _:
            with self.assertRaises(SystemExit) as context:
                CommunicationNetwork.from_json(self.dummy_file)

            self.assertEqual(
                "Line: 3, Chan_id: 4. Participants column empty.",
                str(context.exception),
            )

    def test_from_json_wrong_datetime(self):
        """
        Testing if the from_json function works as expected when the value for datetime is incorrect
        """
        data = {
            "1": {"end": "2020-02-05T12:49:39", "participants": [0.1]},
            "2": {"end": "2020-02-05T12:49:39", "participants": [2, 3]},
            "3": {"end": "hejsan", "participants": ["2"]},
            "4": {"end": "2020-02-05T12:49:59", "participants": [3]},
            "5.3": {"end": "2020-02-05T12:49:59", "participants": [3, 7]},
        }

        with patch(self.json_function_used, return_value=data) as _:
            with self.assertRaises(SystemExit) as context:
                CommunicationNetwork.from_json(self.dummy_file)

            self.assertEqual(
                "Line: 2, Chan_id: 3. End column not compatible datetime format.",
                str(context.exception),
            )


class TestCommunicationNetworkIntegration(unittest.TestCase):
    """
    A test case for the CommunicationNetwork class.
    """

    def setUp(self):
        """
        Differentiating between normal json and orjson depending on which is installed.
        Creating a compressed dummy file and an uncompressed dummy file.
        Defining the data used for the tests
        """
        try:
            import orjson

            self.json_function_used = "orjson.loads"
        except:
            self.json_function_used = "json.loads"

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
            "12": {"end": "2020-02-05T12:49:35", "participants": [9, 8]},
        }

    def tearDown(self):
        """
        Removing both files created in the setup
        """
        os.remove(self.dummy_file_compressed)
        os.remove(self.dummy_file_uncompressed)

    def test_from_json_compressed_integration(self):
        """
        Testing if the from_json function works as expected when the values are compressed and correct
        """
        with patch(self.json_function_used, return_value=self.data) as _:
            com_net = CommunicationNetwork.from_json(self.dummy_file_compressed)

            self.assertEqual(com_net.name, None)

            self.assertSetEqual(
                com_net.channels(),
                {
                    "00",
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                },
            )
            self.assertSetEqual(com_net.channels(0), {"00", "10"})
            self.assertSetEqual(com_net.channels(5), {"02", "07", "11"})
            self.assertSetEqual(com_net.channels(9), {"04", "10", "12"})

            self.assertSetEqual(
                com_net.participants(), {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11}
            )
            self.assertSetEqual(com_net.participants("00"), {0, 1})
            self.assertSetEqual(com_net.participants("04"), {7, 8, 9})
            self.assertSetEqual(com_net.participants("08"), {3})

    def test_from_json_uncompressed_integration(self):
        """
        Testing if the from_json function works as expected when the values are uncompressed and correct
        """
        with patch(self.json_function_used, return_value=self.data) as _:
            com_net = CommunicationNetwork.from_json(self.dummy_file_uncompressed)

            self.assertEqual(com_net.name, None)

            self.assertSetEqual(
                com_net.channels(),
                {
                    "00",
                    "01",
                    "02",
                    "03",
                    "04",
                    "05",
                    "06",
                    "07",
                    "08",
                    "09",
                    "10",
                    "11",
                    "12",
                },
            )
            self.assertSetEqual(com_net.channels(0), {"00", "10"})
            self.assertSetEqual(com_net.channels(5), {"02", "07", "11"})
            self.assertSetEqual(com_net.channels(9), {"04", "10", "12"})

            self.assertSetEqual(
                com_net.participants(), {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11}
            )
            self.assertSetEqual(com_net.participants("00"), {0, 1})
            self.assertSetEqual(com_net.participants("04"), {7, 8, 9})
            self.assertSetEqual(com_net.participants("08"), {3})
