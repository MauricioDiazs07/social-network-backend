from src.database.db import get_connection

QUERY_INTEREST_LIST = """ SELECT "ID" FROM "T_CATALOGUE_INTEREST" """

QUERY_INTEREST = """ SELECT "INTEREST_ID" FROM "T_USER_INTEREST" """
QUERY_GENDER = """ SELECT "GENDER" FROM "T_PROFILE" """
QUERY_BIRTHDATE_AND_SECCION = """ SELECT "BIRTHDATE","SECCION" FROM "T_USER_DATA" """

class DataModel():

    @classmethod
    def get_birthdate_and_seccion(self):
        try:
            conn = get_connection()
            birthdate = []
            seccion = []
            with conn.cursor() as cur:
                cur.execute(QUERY_BIRTHDATE_AND_SECCION)
                resultset = cur.fetchall()
                for row in resultset:
                    birthdate.append(row[0])
                    seccion.append(row[1])
            conn.close()
            return birthdate, seccion
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_gender(self):
        try:
            conn = get_connection()
            gender = []
            with conn.cursor() as cur:
                cur.execute(QUERY_GENDER)
                resultset = cur.fetchall()
                for row in resultset:
                    gender.append(row[0])
            conn.close()
            return gender
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