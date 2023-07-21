from src.database.db import get_connection
from .entities.catalogue.Catalogue import Catalogue

ALL_INTERESTS_QUERY = """ SELECT * FROM "T_CATALOGUE_INTEREST" """
ADD_INTEREST = """ INSERT INTO "T_USER_INTEREST" ("PROFILE_ID","INTEREST_ID") VALUES """

class InterestModel():

    @classmethod
    def get_all(self):
        try:
            conn = get_connection()
            users = []
            with conn.cursor() as cur:
                cur.execute(ALL_INTERESTS_QUERY)
                resultset = cur.fetchall()

                for row in resultset:
                    user = Catalogue(row[0],row[1])
                    users.append(user.to_JSON())

            conn.close()
            return users
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def add_interests(self, interests):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                argument_string = ",".join("('%s', '%s')" % (x, y) for (x, y) in interests)
                cur.execute(ADD_INTEREST + argument_string )
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)