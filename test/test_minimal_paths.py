import unittest
from random import randint

from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType

def communication_network_fuzzer():
    length = randint(10, 200)
    input_network: dict = {}
    input_timings: dict = {}
    used: list = []
    for i in range(length):
        check = False
        while check is False:
            other_vertex = randint(0, length)
            if other_vertex == i:
                other_vertex += 1
            participant: list = ["v" + str(i), "v" + str(other_vertex)]
            participantreverse: list = ["v" + str(other_vertex), "v" + str(i)]
            if participant not in used and participantreverse not in used:
                used.append(participant)
                used.append(participantreverse)
                input_network["h" + str(i)] = participant
                input_timings["h" + str(i)] = randint(1, 200)
                check = True
    return input_network, input_timings


class MinimalPath(unittest.TestCase):
    fuzzed_input = communication_network_fuzzer()
    cn = CommunicationNetwork(fuzzed_input[0], fuzzed_input[1])
    cn_dummy = CommunicationNetwork({'h0': ['v0', 'v1'], 'h1': ['v1', 'v9'], 'h2': ['v2', 'v6'], 'h3': ['v3', 'v8'], 'h4': ['v4', 'v3'], 'h5': ['v5', 'v6'], 'h6': ['v6', 'v7'], 'h7': ['v7', 'v0'], 'h9': ['v9', 'v8'], 'h10': ['v10', 'v8']}, {'h0': 176, 'h1': 68, 'h2': 187, 'h3': 163, 'h4': 57, 'h5': 160, 'h6': 111, 'h7': 174, 'h8': 82, 'h9': 49, 'h10': 7})


    def test_shortest_same_output(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_fastest_same_output(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_foremost_same_output(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_correct_shortest_output(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn_dummy, 'v4', DistanceType.SHORTEST, min_timing=0), {'v3': 1, 'v8': 2})

    def test_correct_fastest_output(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn_dummy, 'v4', DistanceType.FASTEST, min_timing=0), {'v3': 0, 'v8': 106})

    def test_correct_foremost_output(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn_dummy, 'v4', DistanceType.FOREMOST, min_timing=0), {'v3': 57, 'v8': 163})