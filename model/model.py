import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.id_map = {}

    def create_graph(self, min, max):
        all_pilots = DAO.getAllPilotsInPeriod(min, max)
        print(all_pilots)
        for pilot in all_pilots:
            self.id_map[pilot.id] = pilot

        self.graph.clear()
        self.graph.add_nodes_from(all_pilots)

        edges = DAO.getAllEdges(min, max)
        for start_id, destination_id, weight in edges:
            self.graph.add_edge(self.id_map[start_id], self.id_map[destination_id], weight=weight)