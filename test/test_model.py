import unittest
from unittest.mock import MagicMock, patch
import bz2
from pathlib import Path
from datetime import datetime
import json
from simulation.model import CommunicationNetwork, TimeVaryingHypergraph

# class CommunicationNetworkTest(unittest.TestCase):

#     cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

#     def test_setup(self):
#         self.assertEqual(len(self.cn.vertices()), 4)
#         self.assertEqual(self.cn.vertices('h1'), {'v1', 'v2'})

#     def test_channels(self):
#         self.assertEqual(len(self.cn.vertices()), 4)
#         self.assertEqual(self.cn.vertices('h1'), {'v1', 'v2'})

#     def test_participants(self):
#         self.assertEqual(len(self.cn.hyperedges()), 3)
#         self.assertEqual(self.cn.hyperedges('v1'), {'h1'})


class TimeVaryingHypergraphTest(unittest.TestCase):
    cn = TimeVaryingHypergraph(
        {"h1": ["v1", "v2"], "h2": ["v2", "v3"], "h3": ["v3", "v4"]},
        {"h1": 1, "h2": 2, "h3": 3},
    )

    def test_timings(self):
        self.assertEqual(len(self.cn.timings()), 3)
        self.assertEqual(self.cn.timings("h1"), 1)

    def test_vertices(self):
        self.assertEqual(len(self.cn.vertices()), 4)
        self.assertEqual(self.cn.vertices("h1"), {"v1", "v2"})

        with self.assertRaises(Exception) as context:
            self.cn.vertices("x1")
        self.assertTrue("Unknown hyperedge x1" in str(context.exception))

    def test_hyperedges(self):
        self.assertEqual(len(self.cn.hyperedges()), 3)
        self.assertEqual(self.cn.hyperedges("v1"), {"h1"})

        with self.assertRaises(Exception) as context:
            self.cn.hyperedges("x1")
        self.assertTrue("Unknown vertex x1" in str(context.exception))


class CommunicationNetworkTest(unittest.TestCase):
    def test_from_json(self):
        # Mock the file reading and decompression
        mock_file = MagicMock()
        mock_file_path = MagicMock(spec=Path)
        mock_file_path.suffix = ".bz2"
        mock_file_path.open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = bz2.compress(
            b"""{
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
            }"""
        )
        mock_data = {
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
        mock_json_loads = MagicMock(return_value=mock_data)

        # Patch the required functions and objects with the mocks
        with patch("builtins.open", return_value=mock_file), patch(
            "json.loads", mock_json_loads
        ), patch("simulation.model.Path", spec=Path) as mock_path:
            # Set up the mock Path object
            mock_path.return_value = mock_file_path
            mock_file_path.suffix = ".bz2"
            mock_file_path.open.return_value.__enter__.return_value = mock_file

            # Import the module or class that contains the method to be tested

            # Call the method to be tested
            result = CommunicationNetwork.from_json(mock_file_path)

            # Assert the expected behavior or outcome
            self.assertEqual(result.name, None)
            self.assertEqual(result.channels(), {"channel1"})
            self.assertEqual(
                result.participants(),
                {1, 2, 3},
            )

            # Assert the expected function calls were made
            mock_file_path.open.assert_called_once_with("rb")
            mock_file.read.assert_called_once_with()

            # Additional assertions or tests can be performed as needed

class Test:
    cls = {"00": {"end": "2020-02-05T12:49:39", "participants": [0, 1]}}

    @classmethod
    # should fail
    def read_data_1(cls):
        raw_data = json.loads(cls)
        print(raw_data)

    @classmethod
    # should pass
    def read_data_2(cls):
        raw_data = json.loads(cls)
        assert isinstance(raw_data['participants'], int)
        print(raw_data)

    @classmethod
    # should pass
    def read_data_3(cls):
        raw_data = json.loads(cls)
        try:
            datetime.fromisoformat("2020-02-05T12:49:39")
            assert isinstance(raw_data['end'], datetime)
        except ValueError:
            0
        
class TestReadData(unittest.TestCase):
    base_test = """{"test":0}"""
    def test_read_data_1(self):
        with patch('json.loads', return_value={'test':1.0}) as _:
            with self.assertRaises(Exception):
                Test.read_data_1()

    def test_read_data_2(self):
        with patch('json.loads', return_value={'test':1.0}) as _:
            with self.assertRaises(Exception):
                Test.read_data_2()

    def test_read_data_2(self):
        with patch('json.loads', return_value={'test':1.0}) as _:
            with self.assertRaises(Exception):
                Test.read_data_3()

