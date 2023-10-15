from src.database.db import get_connection

QUERY_INTEREST_LIST = """ SELECT "ID" FROM "T_CATALOGUE_INTEREST" """

QUERY_INTEREST = """ SELECT "INTEREST_ID" FROM "T_USER_INTEREST" """
QUERY_GENDER = """ SELECT "GENDER" FROM "T_PROFILE" """
QUERY_BIRTHDATE_AND_SECCION = """ SELECT "BIRTHDATE","SECCION" FROM "T_USER_DATA" """

class DataModel():

    @classmethod
    def get_interest_list(self):
        try:
            conn = get_connection()
            interest = []
            with conn.cursor() as cur:
                cur.execute(QUERY_INTEREST_LIST)
                resultset = cur.fetchall()
                for row in resultset:
                    interest.append(row[0])
            conn.close()
            return interest
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_interest(self):
        try:
            conn = get_connection()
            interest = []
            with conn.cursor() as cur:
                cur.execute(QUERY_INTEREST)
                resultset = cur.fetchall()
                for row in resultset:
                    interest.append(row[0])
            conn.close()
            return interest
        except Exception as ex:
            raise Exception(ex)