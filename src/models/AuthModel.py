from src.database.db import get_connection
from .entities.auth.AuthUser import AuthUser

PROFILE_QUERY = """ INSERT INTO "T_PROFILE" ("ID","EMAIL","PASSWORD","ROLE_ID","NAME","GENDER","PROFILE_PHOTO","PHONE_NUMBER", "AREA_CODE") VALUES (%s,%s,%s,1,%s,%s,%s,%s,%s) """
USER_QUERY = """ INSERT INTO "T_USER_DATA" ("PROFILE_ID","STATE","MUNICIPALITY","ADDRESS","BIRTHDATE","CURP","IDENTIFICATION_PHOTO","SECTION") VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
LOGIN_QUERY = """ SELECT "T_PROFILE"."ID", "EMAIL", "NAME", "ROLE_ID", "VERIFIED_PHONE"  FROM "T_PROFILE" INNER JOIN "T_USER_DATA" ON "T_PROFILE"."ID" = "T_USER_DATA"."PROFILE_ID" WHERE "PHONE_NUMBER" = %s AND "PASSWORD" = %s """
VERIFIED = """ UPDATE "T_USER_DATA" SET "VERIFIED_PHONE" = TRUE WHERE "PROFILE_ID" = %s  """

class AuthModel():

    @classmethod
    def login(self, login):
        try:
            conn = get_connection()
            authenticated_user = None
            with conn.cursor() as cur:
                cur.execute(LOGIN_QUERY, (login.phone , login.password))
                result = cur.fetchone()
                if result != None:
                    authenticated_user = AuthUser(result[0],result[1],result[2],result[3],result[4])
                conn.commit()
            conn.close()
            return authenticated_user
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def verified_accound(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(VERIFIED, (profile_id, ))
                result = cur.rowcount
                conn.commit()
            conn.close()
            return result
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def signup(self, signup):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                print("PROFILE")
                cur.execute( PROFILE_QUERY, (signup.id,signup.email,signup.password, signup.name,signup.gender,signup.profile_photo,signup.phone))
                print("USER")
                cur.execute( USER_QUERY, (signup.id,signup.state,signup.municipality,signup.address,signup.birthdate,signup.curp,signup.identification_photo,signup.section))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)