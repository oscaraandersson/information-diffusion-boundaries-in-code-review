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
        num_verticies = randint(1, 10)
        while num_verticies != 0:
            other_vertex = str(randint(0, length))
            participant: list = ["v" + str(i), "v" + other_vertex]
            participantreverse: list = ["v" + other_vertex, "v" + str(i)]
            if participant not in used and participantreverse not in used:
                used.append(participant)
                used.append(participantreverse)
                input_network["h" + str(i)] = participant
            num_verticies = num_verticies - 1
        input_timings["h" + str(i)] = randint(1, 200)
    return input_network, input_timings


class MinimalPath(unittest.TestCase):
    fuzzed_input = communication_network_fuzzer()
    print(fuzzed_input[0])
    cn = CommunicationNetwork(fuzzed_input[0], fuzzed_input[1])

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
