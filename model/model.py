import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapA = {}

    def buildGraph(self):
        self._graph.clear()
        nodi = DAO.getAllNodes()
        for a in nodi:
            self._idMapA[a.AlbumId] = a
        self._graph.add_nodes_from(nodi)

        edges = DAO.getAllEdges(self._idMapA)
        for e1,e2 in edges:      #DATO CHE E' UNA TUPLA DEVO FARE COSì OPPURE FACCIIO ADD EDGES FROM(EDGES)
            self._graph.add_edge(e1, e2)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getComponentiConnesse(self):
        #nx.number_connected_components(self._graph) anche cosi per numero componente connessa

        components = list(nx.connected_components(self._graph))  # len --> numero componenti connesse
        largest = max(components, key=len)  # usa la dimensione della componente per decidere qual è la più grande. Mi da tutti i nodi
                                            #len largest mi da quanti ce ne sono
        return len(components), largest

    def getInfoComponenteLargest(self):
        c, largest = self.getComponentiConnesse()

        result = []
        for album in sorted(largest, key=lambda a: a.Title):
            result.append(str(album))

        #result.sort(key = lambda x: x[1])
        return result

    def getAlbum(self):
        return self._graph.nodes()

        # =====================================================================
        # PUNTO 2: N ALBUM IN COMPONENTI DIVERSE, MAX NUMERO DI BRANI
        # (famiglia C, schema "per componente": la salto / la prendo)
        # =====================================================================

    def getBestSelection(self, starting_album, N):
        # AZZERO il migliore a ogni ricerca (il prof non lo fa: bug)
        self._bestSelection = []
        self._maxTracks = 0

        if starting_album not in self._graph.nodes or N < 1:
            return [], 0  # sempre DUE valori

        # tutte le componenti TRANNE quella dell'album di partenza
        # (la sua è già "usata" dal primo album)
        comp_rimanenti = [c for c in nx.connected_components(self._graph)
                          if starting_album not in c]

        parziale = [starting_album]  # il primo album è fissato dal testo
        self._ricorsione(parziale, N, comp_rimanenti)
        return self._bestSelection, self._maxTracks

    def _ricorsione(self, parziale, N, comp_rimanenti):
        # (1) CASO TERMINALE: ho esattamente N album -> valuto e mi fermo
        if len(parziale) == N:
            tot = self._getTotalTracks(parziale)
            if tot > self._maxTracks:
                self._maxTracks = tot
                self._bestSelection = copy.deepcopy(parziale)  # COPIA: parziale cambia
            return

        # (2) POTATURA: mancano più album di quante componenti restano
        #     (copre anche "componenti finite" e N > numero componenti)
        if N - len(parziale) > len(comp_rimanenti):
            return

        # (3) decido sulla PRIMA componente rimasta: così ogni componente
        #     è considerata una sola volta
        nextComp = comp_rimanenti[0]

        # (4) RAMO "LA SALTO": non prendo niente da nextComp.
        #     comp_rimanenti[1:] è una lista NUOVA -> niente pop per lei
        self._ricorsione(parziale, N, comp_rimanenti[1:])

        # (5) RAMO "LA PRENDO": da una componente conviene sempre l'album
        #     con PIÙ brani (la somma si spezza per componente)
        best_album = self._getAlbumWithMostTracks(nextComp)
        if best_album is not None:
            parziale.append(best_album)
            self._ricorsione(parziale, N, comp_rimanenti[1:])
            parziale.pop()  # backtracking
