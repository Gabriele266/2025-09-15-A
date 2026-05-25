import copy

import networkx as nx

from database.DAO import DAO
from model import driver


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapDrivers ={}
        self._drivers = []
        self._optListPiloti = None
        self._minDistGiorni = None

    def getListaPilotiOttima(self, k):
        self._optListPiloti = []
        self._minDistGiorni = 100*365

        components = list(nx.connected_components(self._graph))

        if len(components) < k:
            # allora non ho abbastanza componenti connesse da cui pescare, e non posso trovare una sol
            return None, 0

        parziale = []
        self._ricorsione(components, k, parziale,0 )
        return self._optListPiloti, self._minDistGiorni

    def _ricorsione(self, components, k, parziale, indexComponente):
        # condizione di ottimalità
        if len(parziale) == k:
            # ho una soluzione accettabile.
            dateDiNascita = [p.dob for p in parziale]
            diffEtaPiloti = (max(dateDiNascita) - min(dateDiNascita)).days
            if diffEtaPiloti < self._minDistGiorni:
                self._optListPiloti = copy.deepcopy(parziale)
                self._minDistGiorni = diffEtaPiloti
            return

        #condizione di terminazione
        #1) esco se l'indice che indica quale comp connessa sto considerando a questa iterazione è diventato maggiore o
        #uguale al numero di componenti connesse totali, perchè vuol dire che non ho altre componenti connesse da cui pescare
        #2) l'altro motivo è se non ho abbastanza componenti rimanenti per arrivare a k piloti in parziale
        if indexComponente >= len(components) or (len(components) - indexComponente) < (k-len(parziale)):
            return

        # se non sono uscito, allora posso aggiungere ancora piloti. Per questa componente, di indice indexComponente,
        # provo ad ingaggiare un pilota oppure a non ingaggiare nessuno.

        #caso 1, inserisco un pilota appartenente a questa comp connessa. In questo branch provo tutti i piloti che
        # fanno parte della componente connessa in esame.
        componente = components[indexComponente]
        for pilota in componente:
            parziale.append(pilota)
            self._ricorsione(components, k, parziale, indexComponente+1)
            parziale.pop()

        #caso 2, mi tengo un brach di esplorazione in cui io non ho preso proprio nessuno da questa comonente.
        self._ricorsione(components, k, parziale, indexComponente+1)

    def buildGraph(self, year1, year2):
        self._graph.clear()

        self._drivers = DAO.getAllNodes(year1, year2)
        for d in self._drivers:
            self._idMapDrivers[d.driverId] = d

        self._graph.add_nodes_from(self._drivers)

        edges = DAO.getAllEdges(year1, year2, self._idMapDrivers)
        for e in edges:
            self._graph.add_edge(e.d1, e.d2, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop3Archi(self):
        return sorted(self._graph.edges(data=True), key= lambda x: x[2]["weight"], reverse=True)[:3]

    def getConnessaInfo(self):

        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)

        subgraph = self._graph.subgraph(largest).copy()

        orderedNodes = sorted(subgraph.nodes(), key= lambda n: self._graph.degree(n), reverse=True)

        details = [(n, self._graph.degree(n)) for n in orderedNodes]
        return len(components), largest, details

    def getAllYears(self):
        return DAO.getAllYears()