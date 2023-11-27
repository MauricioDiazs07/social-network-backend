from src.database.db import get_connection
from src.models.entities.master.Master import Master

DATA = """ SELECT "NAME", "DESCRIPTION", "PROFILE_PHOTO", "EMAIL" FROM "T_PROFILE" WHERE "ID" = %s """
UPDATE_PHOTO = """ UPDATE "T_PROFILE" SET "NAME" = %s, "EMAIL"= %s, "DESCRIPTION" = %s, "PROFILE_PHOTO" = %s WHERE  "ID" = %s; """
UPDATE = """ UPDATE "T_PROFILE" SET "NAME" = %s, "EMAIL"= %s, "DESCRIPTION" = %s WHERE  "ID" = %s; """

class MasterModel():

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