from src.database.db import get_connection
from .entities.catalogue.Catalogue import Catalogue

FEELINGS = """ SELECT * FROM "T_CATALOGUE_FEELING" """
INTERESTS = """ SELECT * FROM "T_CATALOGUE_INTEREST" """

class CatalogueModel:

    @classmethod
    def feeling_data(self):
        try:
            conn = get_connection()
            interest = []
            with conn.cursor() as cur:
                cur.execute(FEELINGS)
                resultset = cur.fetchall()
                for row in resultset:
                    user = Catalogue(row[0],row[1])
                    interest.append(user.to_JSON())
            conn.close()
            return interest
        except Exception as ex:
            raise Exception(ex)

    @classmethod  
    def interest_data(self):
        try:
            conn = get_connection()
            interest = []
            with conn.cursor() as cur:
                cur.execute(INTERESTS)
                resultset = cur.fetchall()
                for row in resultset:
                    user = Catalogue(row[0],row[1])
                    interest.append(user.to_JSON())
            conn.close()
            return interest
        except Exception as ex:
            raise Exception(ex)