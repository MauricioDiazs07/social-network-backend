from src.database.db import get_connection
from src.models.entities.master.Master import Master
from .entities.auth.AuthUser import AuthUser

DATA = """ SELECT "NAME", "DESCRIPTION", "PROFILE_PHOTO", "EMAIL" FROM "T_PROFILE" WHERE "ID" = %s """
UPDATE_PHOTO = """ UPDATE "T_PROFILE" SET "NAME" = %s, "EMAIL"= %s, "DESCRIPTION" = %s, "PROFILE_PHOTO" = %s WHERE  "ID" = %s; """
UPDATE = """ UPDATE "T_PROFILE" SET "NAME" = %s, "EMAIL"= %s, "DESCRIPTION" = %s WHERE  "ID" = %s; """

DATA_LOGIN = """ SELECT "ID", "EMAIL", "NAME", "ROLE_ID", "PASSWORD" FROM "T_PROFILE" WHERE "ID" = (
SELECT "MASTER_ID" FROM "T_MASTER" WHERE "ADMIN_ID" = %s) """

class MasterModel():

    @classmethod
    def get_login_info(self, admin_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DATA_LOGIN, (admin_id,))
                result = cur.fetchone()
                authenticated_user = AuthUser(result[0],result[1],result[2],result[3],result[4])
            conn.close()
            return authenticated_user
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_info(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DATA, (profile_id,))
                row = cur.fetchone()
                master = Master(row[0],row[1],row[2],row[3])
            conn.close()
            master = master.to_JSON()
            master['profile_photo'] = master['profile_photo'][0]
            return master
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update(self, profile_id,name,email,description):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE, (name, email,description,profile_id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_photo(self, profile_id,name,email,description,profile_photo):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE_PHOTO, (name,email,description,profile_photo,profile_id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)