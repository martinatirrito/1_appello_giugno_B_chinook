import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):

        try:
            self._model.buildGraph()
            self._view._txt_result.controls.clear()
            Nnodi, Narchi = self._model.getGraphDetails()
            self._view._txt_result.controls.append(
                ft.Text("Grafo correttamente creato.")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di nodi: {Nnodi}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di archi: {Narchi}")
            )

            self.fillDDAlbums()

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")


    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()

        nNodi, nArchi = self._model.getGraphDetails()

        if nNodi == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        try:
            num_components, largest = self._model.getComponentiConnesse()
            self._view._txt_result.controls.append(
                ft.Text(f"Numero di componenti connesse: {num_components}"))

            self._view._txt_result.controls.append(ft.Text(f""))

            self._view._txt_result.controls.append(ft.Text(f"Dimensione della componente connessa più grande: {len(largest)} album"))

            self._view._txt_result.controls.append(ft.Text(f""))

            self._view._txt_result.controls.append(ft.Text(f"Dettagli degli album appartenenti alla componente connessa più grande: "))
            self._view._txt_result.controls.append(ft.Text(f""))
            self._view._txt_result.controls.append(ft.Text(f""))
            listaAlbum = self._model.getInfoComponenteLargest()
            for album in listaAlbum:
                self._view._txt_result.controls.append(ft.Text(str(album)))

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")

    def fillDDAlbums(self):
        self._view._ddAlbum.options.clear()
        album = self._model.getAlbum()
        for a in album:
            self._view._ddAlbum.options.append(ft.dropdown.Option(str(a.AlbumId), text=str(a)))

        self._view.update_page()

    def handleSelezione(self,e):
        pass