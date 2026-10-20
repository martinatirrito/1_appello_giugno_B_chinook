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
