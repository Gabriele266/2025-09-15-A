from database.DB_connect import DBConnect
from model.Edge import Edge
from model.Pilot import Pilot


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllPilotsInPeriod(min_year: int, max_year: int)-> list[Pilot]:
        query = """
        SELECT RE.driverId, COUNT(*) as numero_gare, DV.driverRef 
        FROM results RE, drivers DV, races RS
            WHERE RE.raceId = RS.raceId AND 
            RE.driverId = DV.driverId AND
            RE.position IS NOT NULL	AND
            RS.year BETWEEN %s AND %s
            GROUP BY RE.driverId;
        """

        data = tuple([min_year, max_year])
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary = True)
        cursor.execute(query, data)

        p = []
        for row in cursor:
            p.append(Pilot(row["driverId"], row["driverRef"]))

        cursor.close()
        connection.close()
        return p

    @staticmethod
    def getAllEdges(min_year: int, max_year: int)-> list[tuple[int, int, int]]:
        query = """
        SELECT REA.driverId as driver_a, REB.driverId as driver_b, COUNT(*) as weight
        FROM results REA, drivers DVA, races RSA,
            results REB, drivers DVB, races RSB
            WHERE REA.raceId = RSA.raceId AND 
            REA.driverId = DVA.driverId AND
            REA.position IS NOT NULL	AND			
            RSA.year BETWEEN %s AND %s AND	
            REB.raceId = RSB.raceId AND 
            REB.driverId = DVB.driverId AND
            REB.position IS NOT NULL	AND	
            RSB.year BETWEEN %s AND %s AND
            REA.driverId > REB.driverId AND		
            REA.raceId = REB.raceId AND			
            REA.constructorId = REB.constructorId
            GROUP BY REA.driverId, REB.driverId;
        """
        data = tuple([min_year, max_year, min_year, max_year])
        connection = DBConnect.get_connection()
        cursor = connection.cursor(dictionary = True)
        cursor.execute(query, data)

        edges = []
        for row in cursor:
            edges.append((
                row["driver_a"],
                row["driver_b"],
                row["weight"]
            ))

        cursor.close()
        connection.close()
        return edges