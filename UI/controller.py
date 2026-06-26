import time

import flet as ft
import networkx as nx

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def populateDDAnni(self):
        anni = DAO.getAllYears()
        dd1: ft.Dropdown = self._view._ddAnno1
        dd2: ft.Dropdown = self._view._ddAnno2

        dd1.options = [
            ft.dropdown.Option(key=a, text=a) for a in anni
        ]

        dd2.options = [
            ft.dropdown.Option(key=a, text=a) for a in anni
        ]

    def handleCreaGrafo(self,e):
        dd1: ft.Dropdown = self._view._ddAnno1
        dd2: ft.Dropdown = self._view._ddAnno2

        a1 = dd1.value
        a2 = dd2.value

        if a1 is None or a2 is None or a1 > a2:
            self._view.create_alert("Selezionare un range di date valide")
            return

        self._model.create_graph(int(a1), int(a2))
        txt_result: ft.ListView = self._view.txt_result
        txt_result.controls = [
            ft.Text("Grafo correttamente creato"),
            ft.Text(f"Il grafo ha {self._model.graph.number_of_nodes()} nodi e {self._model.graph.number_of_edges()} archi")
        ]

        self._view.update_page()

    def handleDettagli(self, e):
        if self._model.graph is None:
            self._view.create_alert("Il grafo non è stato creato")
            return

        archi_peso_maggiore = self._model.get_best_edges()
        print(archi_peso_maggiore)
        txt_result: ft.ListView = self._view.txt_result
        txt_result.controls.append(
            ft.Text("Archi con peso maggiore", color="red"))

        for start, end, data in archi_peso_maggiore:
            txt_result.controls.append(
            ft.Text(f"{start.name} -> {end.name} con peso {data["weight"]}")
        )

        txt_result.controls.append(ft.Text(f"\nNumero di componenti connesse: {nx.number_connected_components(self._model.graph)}", size=20, color="red"))
        nds = self._model.get_biggest_connected_component_nodes()
        txt_result.controls.append(ft.Text(f"La componente connessa più grande ha {len(nds)} nodi", size=18, color="red"))
        for node in nds:
            txt_result.controls.append(ft.Text(node.__str__()))

        self._view.update_page()

    def handleCerca(self, e):
        if self._model.graph is None:
            self._view.create_alert("Il grafo non è stato creato")
            return

        v = self._view._txtInK.value
        if v is None or v == '':
            self._view.create_alert("Selezionare un valore per K")
            return

        # Prendo tutte le n componenti connesse
        # Ho un insieme massimo di K piloti
        # Prendo un pilota da ogni componente connessa, esplorando tutte le combinazioni
        t1 = time.time()
        res = self._model.search_best_set(int(v))
        t2 = time.time()

        txt_result: ft.ListView = self._view.txt_result

        if res is not None and res != []:
            txt_result.controls.append(ft.Text("\nHo trovato una soluzione", color="red", size=22))
            txt_result.controls.append(ft.Text(f"Tempo impiegato {t2 - t1} secondi", color="gray", size=17))

            for node in res:
                txt_result.controls.append(ft.Text(node))

            txt_result.controls.append(ft.Text(f"Con differenza di età {self._model.best_dob.days / 365} anni"))
        else:
            txt_result.controls.append(ft.Text("La soluzione non esiste, il problema è impossibile. Controllare il numero di componenti connesse. "))

        self._view.update_page()
