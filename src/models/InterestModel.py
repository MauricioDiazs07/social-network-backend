from src.database.db import get_connection
from .entities.catalogue.Catalogue import Catalogue
from src.models.entities.interest.Interest import Interest

ALL_INTERESTS_QUERY = """ SELECT * FROM "T_CATALOGUE_INTEREST" """
ADD_INTEREST = """ INSERT INTO "T_USER_INTEREST" ("PROFILE_ID","INTEREST_ID") VALUES """
CLEAN_INTEREST = """ DELETE FROM "T_USER_INTEREST" WHERE "PROFILE_ID" = '{}' """
GET_INTEREST = """ SELECT "INTEREST_ID", "DESCRIPTION" FROM "T_USER_INTEREST" INNER JOIN "T_CATALOGUE_INTEREST" ON "T_USER_INTEREST"."INTEREST_ID" = "T_CATALOGUE_INTEREST"."ID" WHERE "PROFILE_ID" = '{}' """

class InterestModel():

    @classmethod
    def get_all(self):
        try:
            conn = get_connection()
            interest = []
            with conn.cursor() as cur:
                cur.execute(ALL_INTERESTS_QUERY)
                resultset = cur.fetchall()

                for row in resultset:
                    user = Catalogue(row[0],row[1])
                    interest.append(user.to_JSON())

            conn.close()
            return interest
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
    
    @classmethod
    def clean_interests(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(CLEAN_INTEREST.format(profile_id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_interests(self, profile_id):
        try:
            conn = get_connection()
            interest_list = []
            with conn.cursor() as cur:
                cur.execute(GET_INTEREST.format(profile_id))
                resultset = cur.fetchall()

                for row in resultset:
                    interest = Interest(row[0],row[1])
                    interest_list.append(interest.to_JSON())
            conn.close()
            data = {"profile_id": profile_id, "interest_list": interest_list}
            return data
        except Exception as ex:
            raise Exception(ex)