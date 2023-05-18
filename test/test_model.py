import unittest
import json
from simulation.model import CommunicationNetwork, TimeVaryingHypergraph
from unittest.mock import patch, mock_open


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

    cn = TimeVaryingHypergraph({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_timings(self):
        self.assertEqual(len(self.cn.timings()), 3)
        self.assertEqual(self.cn.timings('h1'), 1)

    def test_vertices(self):
        self.assertEqual(len(self.cn.vertices()), 4)
        self.assertEqual(self.cn.vertices('h1'), {'v1', 'v2'})

        with self.assertRaises(Exception) as context:
            self.cn.vertices('x1')
        self.assertTrue('Unknown hyperedge x1' in str(context.exception))

    def test_hyperedges(self):
        self.assertEqual(len(self.cn.hyperedges()), 3)
        self.assertEqual(self.cn.hyperedges('v1'), {'h1'})

        with self.assertRaises(Exception) as context:
            self.cn.hyperedges('x1')
        self.assertTrue('Unknown vertex x1' in str(context.exception))

class ModelDataTest(unittest.TestCase):
    def test_model_with_data(self):
        dummy_json = """{"00":{"end":"2020-02-05T12:49:39","participants":[0,1]},
          "01":{"end":"2020-02-05T12:49:49","participants":[2,3]},
          "02":{"end":"2020-02-05T12:49:59","participants":[4,5]},
          "03":{"end":"2020-02-05T12:49:19","participants":[6]},
          "04":{"end":"2020-02-05T12:49:29","participants":[7,8,9]},
          "05":{"end":"2020-02-05T12:59:39","participants":[1,4]},
          "06":{"end":"2020-02-05T12:59:30","participants":[2,7]},
          "07":{"end":"2020-02-05T12:59:39","participants":[5,2]},
          "08":{"end":"2020-02-05T12:49:31","participants":[3]},
          "09":{"end":"2020-02-05T12:49:32","participants":[8,11]},
          "10":{"end":"2020-02-05T12:49:33","participants":[0,9]},
          "11":{"end":"2020-02-05T12:49:34","participants":[5,6]},
          "12":{"end":"2020-02-05T12:49:35","participants":[9,8]}}"""
    
        fake_file_path = 'file/path/mock'

        with patch('builtins.open', new=mock_open(read_data=dummy_json)) as _file:
            com_network = CommunicationNetwork.from_json(dummy_json)
            _file.assert_called_once_with(fake_file_path, 'r')

        self.assertEqual(len(com_network.participants()), 37103)
        self.assertEqual(len(com_network.channels()), 309740)

        self.assertEqual(len(com_network.vertices()), 37103)
        self.assertEqual(len(com_network.hyperedges()), 309740)
