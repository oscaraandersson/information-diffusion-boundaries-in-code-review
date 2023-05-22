from random import randint
import sys

sys.path.insert(0, '../')

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

def test_shortest_same_output(Cn):
    result_1 = single_source_dijkstra_vertices(Cn, 'v1', DistanceType.SHORTEST, min_timing=0)
    result_2 = single_source_dijkstra_hyperedges(Cn, 'v1', DistanceType.SHORTEST, min_timing=0)
    return result_1, result_2

def test_fastest_same_output(Cn):
    result_1 = single_source_dijkstra_vertices(Cn, 'v1', DistanceType.FASTEST, min_timing=0)
    result_2 = single_source_dijkstra_hyperedges(Cn, 'v1', DistanceType.FASTEST, min_timing=0)
    return result_1, result_2

def test_foremost_same_output(Cn):
    result_1 = single_source_dijkstra_vertices(Cn, 'v1', DistanceType.FOREMOST, min_timing=0)
    result_2 = single_source_dijkstra_hyperedges(Cn, 'v1', DistanceType.FOREMOST, min_timing=0)
    return result_1, result_2


if __name__ == "__main__":
    for run in range(20000):
        fuzzed_input = communication_network_fuzzer()
        cn = CommunicationNetwork(fuzzed_input[0], fuzzed_input[1])
        shortest = test_shortest_same_output(cn)
        fastest = test_fastest_same_output(cn)
        foremost = test_foremost_same_output(cn)
        if shortest[0] != shortest[1]:
            print(f"Shortest path not equal for run {run}.\ndijkstra_vertices output: {shortest[0]}\ndijkstra_hyperedges output: {shortest[1]}")
        if fastest[0] != fastest[1]:
            print(f"Fastest path not equal for run {run}.\ndijkstra_vertices output: {fastest[0]}\ndijkstra_hyperedges output: {fastest[1]}")
        if foremost[0] != foremost[1]:
            print(f"Foremost path not equal for run {run}.\ndijkstra_vertices output: {foremost[0]}\ndijkstra_hyperedges output: {foremost[1]}")
