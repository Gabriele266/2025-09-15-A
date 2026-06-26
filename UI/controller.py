import flet as ft

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
        pass

    def handleCerca(self, e):
        pass

