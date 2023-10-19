from src.database.db import get_connection

QUERY_INTEREST_LIST = """ SELECT "ID" FROM "T_CATALOGUE_INTEREST" """

QUERY_INTEREST = """ SELECT "INTEREST_ID" FROM "T_USER_INTEREST" """
QUERY_GENDER = """ SELECT "GENDER" FROM "T_PROFILE" WHERE "ROLE_ID" = 1 """
QUERY_BIRTHDATE_AND_SECCION = """ SELECT "BIRTHDATE","SECTION" FROM "T_USER_DATA" """

QUERY_SECTIONS_BY_INTEREST_ID = """ SELECT "SECTION" FROM "T_USER_DATA" INNER JOIN "T_USER_INTEREST" ON "T_USER_DATA"."PROFILE_ID" = "T_USER_INTEREST"."PROFILE_ID" WHERE "T_USER_INTEREST"."INTEREST_ID" = %s """
QUERY_INTERESTS_BY_SECTION = """ SELECT "INTEREST_ID" FROM "T_USER_DATA" INNER JOIN "T_USER_INTEREST" ON "T_USER_DATA"."PROFILE_ID" = "T_USER_INTEREST"."PROFILE_ID" WHERE "T_USER_DATA"."SECTION" = %s """


class DataModel():

    @classmethod
    def get_interests_by_section(self, section):
        try:
            conn = get_connection()
            interests = []
            with conn.cursor() as cur:
                cur.execute(QUERY_INTERESTS_BY_SECTION, (section,))
                resultset = cur.fetchall()
                for row in resultset:
                    interests.append(row[0])
            conn.close()
            return interests
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_sections_by_interest_id(self, interest_id):
        try:
            conn = get_connection()
            sections = []
            with conn.cursor() as cur:
                cur.execute(QUERY_SECTIONS_BY_INTEREST_ID, (interest_id,))
                resultset = cur.fetchall()
                for row in resultset:
                    sections.append(row[0])
            conn.close()
            return sections
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_birthdate_and_section(self):
        try:
            conn = get_connection()
            birthdate = []
            section = []
            with conn.cursor() as cur:
                cur.execute(QUERY_BIRTHDATE_AND_SECCION)
                resultset = cur.fetchall()
                for row in resultset:
                    birthdate.append(row[0])
                    section.append(row[1])
            conn.close()
            return birthdate, section
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