import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph: nx.Graph | None = None
        self.id_map = {}

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