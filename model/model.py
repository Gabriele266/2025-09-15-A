import itertools

import networkx as nx

from database.DAO import DAO
from model.Pilot import Pilot


class Model:
    def __init__(self):
        self.graph: nx.Graph | None = None
        self.id_map = {}
        self.best_dob = None
        self.best_set = None

    def create_graph(self, min, max):
        all_pilots = DAO.getAllPilotsInPeriod(min, max)
        print(all_pilots)
        for pilot in all_pilots:
            self.id_map[pilot.id] = pilot

        self.graph = nx.Graph()
        self.graph.add_nodes_from(all_pilots)

        edges = DAO.getAllEdges(min, max)
        for start_id, destination_id, weight in edges:
            self.graph.add_edge(self.id_map[start_id], self.id_map[destination_id], weight=weight)

    def get_best_edges(self):
        # 3 archi con peso maggiore
        all_edges_sorted = sorted(self.graph.edges(data=True), key=lambda edge: edge[2]["weight"], reverse=True)
        return all_edges_sorted[0:3]

    def get_biggest_connected_component_nodes(self) -> list:
        connected_comps = max(nx.connected_components(self.graph), key=len)
        sub_graph = self.graph.subgraph(connected_comps)

        all_nodes = sorted(sub_graph.nodes, key=lambda node: self.graph.degree(node))
        return all_nodes

    def search_best_set(self, k) -> list[Pilot]:
        connected_comps = sorted(nx.connected_components(self.graph), key=len)

        if len(connected_comps) < k:
            return []       # Problema impossibile

        all_pilots = self.graph.nodes

        for combination in itertools.combinations(all_pilots, k):
            if self.check_comb(combination, connected_comps) == True:   # La combinazione ha tutti elementi in componenti connesse distinte
                so = sorted(combination, key=lambda node: node.dob)
                min_dob = so[0].dob
                max_dob = so[-1].dob
                diff = max_dob - min_dob

                if self.best_dob is None or diff < self.best_dob:
                    self.best_dob = diff
                    self.best_set = so.copy()

        return self.best_set

    def check_comb(self, comb, connected_comps):
        for c in comb:
            occurrencies = 0
            for component in connected_comps:
                for node in component:
                    if c == node:
                        occurrencies += 1

            if occurrencies > 1:
                return False        # Ho trovato un nodo che è presente in più componenti connesse

        return True