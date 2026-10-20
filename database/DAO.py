from database.DB_connect import DBConnect
from model.album import Album


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country
                from customer c
                where c.Country is not null
                order by c.Country
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes():
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """select distinct a.*, count(t.TrackId ) as listaBrani
                    from Album a, Track t 
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId
                    order by a.Title asc """

        cursor.execute(query, )

        for row in cursor:
            result.append(Album(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(idMapA):
        try:
            conn = DBConnect.get_connection()
            cursor = conn.cursor(dictionary=True)

        except ConnectionError:
            print("Errore di connessione al databse")
            return

        result = []

        query = """SELECT distinct a1.AlbumId as a1, a2.AlbumId as a2
                    from (select distinct a.AlbumId, t.GenreId  as genere1
                            from Album a, Track t
                            where a.AlbumId = t.AlbumId) as a1, 
                            (select distinct a.AlbumId, t.GenreId as genere2 
                                from Album a, Track t
                                where a.AlbumId = t.AlbumId)as a2
                    where a1.AlbumId < a2.AlbumId 
                    and a1.genere1 = a2.genere2 """



        """In un grafo non orientato (1,5) e (5,1) sono lo stesso arco, 
            quindi ne basta una: < dimezza le righe senza perdere niente.
            In un grafo orientato invece ti servono entrambe, perché poi decidi il verso 
            (es. con il fatturato nella traccia A). Lì usi !=/<>."""

        cursor.execute(query, )

        for row in cursor:
            result.append((idMapA[row["a1"]], idMapA[row["a2"]])) #lista tuple per non pesati

        cursor.close()
        conn.close()
        return result


