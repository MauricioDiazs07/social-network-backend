from src.database.db import get_connection
from .entities.auth.AuthUser import AuthUser

PROFILE_QUERY = """ INSERT INTO "T_PROFILE" ("ID","EMAIL","PASSWORD","ROLE_ID","NAME","GENDER","PROFILE_PHOTO","PHONE_NUMBER", "AREA_CODE") VALUES (%s,%s,%s,1,%s,%s,%s,%s,%s) """
USER_QUERY = """ INSERT INTO "T_USER_DATA" ("PROFILE_ID","STATE","MUNICIPALITY","ADDRESS","BIRTHDATE","CURP","IDENTIFICATION_PHOTO","SECTION") VALUES (%s,%s,%s,%s,%s,%s,%s,%s) """
LOGIN_QUERY = """ SELECT "ID", "EMAIL", "NAME", "ROLE_ID", "PASSWORD" FROM "T_PROFILE" WHERE "PHONE_NUMBER" = %s """
CHECK_VERIFIED = """ SELECT "VERIFIED_PHONE" FROM "T_USER_DATA" WHERE "PROFILE_ID" = %s """
VERIFIED = """ UPDATE "T_USER_DATA" SET "VERIFIED_PHONE" = TRUE WHERE "PROFILE_ID" = %s  """

MASTER_QUERY = """ INSERT INTO "T_PROFILE" ("ID","EMAIL","PASSWORD","ROLE_ID","NAME","GENDER","PROFILE_PHOTO","PHONE_NUMBER", "AREA_CODE") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
ADMIN_QUERY = """ INSERT INTO "T_PROFILE" ("ID","EMAIL","PASSWORD","ROLE_ID","NAME","GENDER","PROFILE_PHOTO","PHONE_NUMBER", "AREA_CODE") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
ADD_ADMIN = """ INSERT INTO "T_MASTER" ("MASTER_ID", "ADMIN_ID") VALUES (%s,%s) """
class AuthModel():

    @classmethod
    def login(self, login):
        try:
            conn = get_connection()
            authenticated_user = None
            with conn.cursor() as cur:
                cur.execute(LOGIN_QUERY, (login.phone,))
                result = cur.fetchone()
                if result != None:
                    authenticated_user = AuthUser(result[0],result[1],result[2],result[3],result[4])
                conn.commit()
            conn.close()
            return authenticated_user
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def check_verified(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(CHECK_VERIFIED, (profile_id, ))
                result = cur.fetchone()
                conn.commit()
            conn.close()
            return result[0]
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
                cur.execute( PROFILE_QUERY, (signup.id,signup.email,signup.password, signup.name,signup.gender,signup.profile_photo,signup.phone, signup.area_code))
                cur.execute( USER_QUERY, (signup.id,signup.state,signup.municipality,signup.address,signup.birthdate,signup.curp,signup.identification_photo,signup.section))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        

    @classmethod
    def create_admin(self, admin):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute( ADMIN_QUERY, (admin.id,admin.email,admin.password, admin.role_id, admin.name,admin.gender,admin.profile_photo,admin.phone_number, admin.area_code))
                cur.execute( ADD_ADMIN, (admin.master_id, admin.id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def create_master(self, master):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute( MASTER_QUERY, (master.id,master.email,master.password,master.role_id, master.name,master.gender,master.profile_photo,master.phone_number, master.area_code))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)