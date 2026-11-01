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

    def handleSelezione(self, e):
        self._view._txt_result.controls.clear()

        # validazione 1: grafo creato
        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        # validazione 2: album scelto
        if self._view._ddAlbum.value is None:
            self._view.create_alert("Selezionare un album.")
            return

        # validazione 3: N intero (anche il campo vuoto "" dà ValueError)
        try:
            N = int(self._view._txtInN.value)
        except ValueError:
            self._view.create_alert("Inserire un numero intero per N.")
            return

        # validazione 4: N almeno 1 (il prof non lo controlla)
        if N < 1:
            self._view.create_alert("N deve essere almeno 1.")
            return

        # stringa -> int -> OGGETTO Album (il Model vuole l'oggetto)
        start = self._model.getAlbumById(int(self._view._ddAlbum.value))
        if start is None:
            self._view.create_alert("Album non presente nel grafo.")
            return

        selezione, tot_brani = self._model.getBestSelection(start, N)  # spacchetto 2 valori

        # nessuna selezione: N più grande del numero di componenti
        if len(selezione) == 0:
            self._view._txt_result.controls.append(ft.Text(
                f"Nessuna selezione trovata: le componenti connesse sono solo "
                f"{self._model.getNumConnectedComponents()}."))
            self._view.update_page()
            return

        self._view._txt_result.controls.append(ft.Text("Album selezionati:"))
        # lista ordinata per titolo
        for album in sorted(selezione, key=lambda a: a.Title):
            # generi dell'album: di solito uno solo, ma 11 album ne hanno più di uno
            generi = sorted({t.GenreId for t in album.Tracks})
            self._view._txt_result.controls.append(ft.Text(
                f"{album.Title} - genere: {', '.join(str(g) for g in generi)} - {len(album.Tracks)} brani"))
        self._view._txt_result.controls.append(ft.Text(f"Numero di album selezionati: {len(selezione)}"))
        self._view._txt_result.controls.append(ft.Text(f"Numero complessivo di brani: {tot_brani}"))
        self._view.update_page()