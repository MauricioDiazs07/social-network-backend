from src.database.db import get_connection
from src.models.entities.admin.Admins import Admins

MASTER_QUERY = """ INSERT INTO "T_PROFILE" ("ID","EMAIL","PASSWORD","ROLE_ID","NAME","GENDER","PROFILE_PHOTO","PHONE_NUMBER", "AREA_CODE") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
ADMIN_QUERY = """ INSERT INTO "T_PROFILE" ("ID","EMAIL","PASSWORD","ROLE_ID","NAME","GENDER","PROFILE_PHOTO","PHONE_NUMBER", "AREA_CODE") VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
ADD_ADMIN = """ INSERT INTO "T_MASTER" ("MASTER_ID", "ADMIN_ID") VALUES (%s,%s) """
LIST_ADMIN = """ 
SELECT "ADMIN_ID","AREA_CODE","PHONE_NUMBER","NAME" 
FROM "T_MASTER" 
INNER JOIN "T_PROFILE" ON "ADMIN_ID" = "T_PROFILE"."ID"
WHERE "MASTER_ID" = %s; """

class AdminModel:

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
    
    @classmethod
    def list_admins(self, master_id):
        try:
            conn = get_connection()
            admins = []
            with conn.cursor() as cur:
                cur.execute( LIST_ADMIN, (master_id,))
                resultset = cur.fetchall()
                for row in resultset:
                    admin = Admins(row[0],row[1],row[2],row[3]).to_JSON()
                    admins.append(admin)
            conn.close()
            return admins
        except Exception as ex:
            raise Exception(ex)