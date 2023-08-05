from src.database.db import get_connection
from .entities.auth.AuthUser import AuthUser

PROFILE_QUERY = """INSERT INTO "T_PROFILE" ("ID","EMAIL","PASSWORD","ROLE_ID","NAME","GENDER") VALUES (%s,%s,%s,1,%s,%s)"""
USER_QUERY = """ INSERT INTO "T_USER_DATA" ("PROFILE_ID","STATE","MUNICIPALITY","ADDRESS","BIRTHDATE","CURP","IDENTIFICATION_PHOTO","PHONE_NUMBER") VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
LOGIN_QUERY = """ SELECT "ID", "EMAIL", "NAME", "ROLE_ID" FROM "T_PROFILE" WHERE "EMAIL" = %s AND "PASSWORD" = %s"""

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
                    authenticated_user = AuthUser(result[0],result[1],result[2],result[3])
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
                cur.execute( PROFILE_QUERY, (signup.id,signup.email,signup.password, signup.name,signup.gender))
                cur.execute( USER_QUERY, (signup.id,signup.state,signup.municipality,signup.address,signup.birthdate,signup.curp,signup.identification_photo,signup.phone))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)