from database.db import get_connection
from .entities.auth.AuthUser import AuthUser

SIGN_UP_QUERY = """INSERT INTO "T_USER" ("EMAIL","PASSWORD", "NAME", "GENDER", "STATE","MUNICIPALITY", "COLONY", "STREET", "INT_NUMBER", "EXT_NUMBER", "BIRTHDATE", "CURP", "IDENTIFICATION_PHOTO") VALUES (%s, %s,%s, %s, %s,%s, %s, %s, %s,%s,%s,%s,%s)"""
LOGIN_QUERY = """SELECT "EMAIL", "NAME", "USER_TYPE" FROM "T_USER" WHERE "EMAIL" = %s AND "PASSWORD" = %s """

class AuthModel():

    @classmethod
    def login(self, login):
        try:
            conn = get_connection()
            authenticated_user = None
            with conn.cursor() as cur:
                cur.execute(LOGIN_QUERY, (login.email , login.password))
                result = cur.fetchone()
                if result != None:
                    authenticated_user = AuthUser(result[0],result[1],result[2])
                conn.commit()
            conn.close()
            return authenticated_user
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def signup(self, signup):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute( SIGN_UP_QUERY, (signup.email,signup.password ,signup.name,signup.gender,signup.state,signup.municipality,signup.colony,signup.street,signup.int_number,signup.ext_number,signup.birthdate,signup.curp,signup.identification_photo))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)