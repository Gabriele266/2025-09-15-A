import itertools

import networkx as nx

from database.DAO import DAO
from model.Pilot import Pilot


class Model:
    def __init__(self):
        self.graph: nx.Graph | None = None
        self.id_map = {}
        self.min_diff_dob = None
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

    def search_best_set(self, K: int) -> list[Pilot] | None:
        if K <= 0:
            return None

        conn_comps = sorted(nx.connected_components(self.graph), key=len)
        num_comps = len(conn_comps)

        if K > num_comps:
            return None

        self.best_set = None
        self.min_diff_dob = None
        visited = []

        self.__pescaggio_comp(0, num_comps, visited, K, conn_comps)
        return self.best_set

    def __pescaggio_comp(self, indice_comp: int, num_conn_comps: int, visited: list[Pilot], K: int, conn_comps: list[set[Pilot]]):
        if len(visited) == K:
            # Condizione di termine con verifica dell'ottimalità
            diff = ((max(visited, key=lambda p: p.dob).dob) - (min(visited, key=lambda p: p.dob).dob)).days

            if self.min_diff_dob is None or diff < self.min_diff_dob:
                self.min_diff_dob = diff
                self.best_set = visited.copy()
        elif indice_comp < num_conn_comps:
            # Posso esplorare una nuova componente
            current_component = conn_comps[indice_comp]
            for pilot in current_component:
                visited.append(pilot)
                self.__pescaggio_comp(indice_comp + 1, num_conn_comps, visited, K, conn_comps)
                visited.pop()

            # Branch non utilizzare la componente
            self.__pescaggio_comp(indice_comp + 1, num_conn_comps, visited, K, conn_comps)