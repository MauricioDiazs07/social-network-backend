from src.database.db import get_connection
from src.models.entities.share.Share import Share


CREATE_SHARE = """ INSERT INTO "T_SHARE" ("PROFILE_ID", "SHARE_TYPE", "DESCRIPTION") VALUES (%s, %s, %s) RETURNING "ID" """
GET_ALL_SHARE = """ SELECT "T_SHARE"."ID","NAME","PROFILE_ID","T_PROFILE"."PROFILE_PHOTO","T_SHARE"."DESCRIPTION","SHARE_TYPE","T_SHARE"."CREATION_DATE" FROM "T_SHARE"  INNER JOIN "T_PROFILE" ON "T_SHARE"."PROFILE_ID" = "T_PROFILE"."ID" ORDER BY "T_SHARE"."CREATION_DATE" ASC """
GET_SHARE = """ SELECT "T_SHARE"."ID","NAME","PROFILE_ID","T_PROFILE"."PROFILE_PHOTO","T_SHARE"."DESCRIPTION","SHARE_TYPE","T_SHARE"."CREATION_DATE" FROM "T_SHARE"  INNER JOIN "T_PROFILE" ON "T_SHARE"."PROFILE_ID" = "T_PROFILE"."ID" WHERE "T_SHARE"."ID" = %s """
DELETE_SHARE = """ delete from "T_SHARE" where "ID" = %s """


class ShareModel():

    @classmethod
    def create_share(self, share):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(CREATE_SHARE, (share.profile_id, share.share_type, share.description))
                post_id = cur.fetchone()[0]
                conn.commit()
            conn.close()
            return post_id
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_share(self, id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(GET_SHARE, (id,))
                result = cur.fetchone()
                if result == None:
                    return {"message": "Share not fount"}
                share = Share(result[0],result[1],result[2], result[3],result[4],result[5],result[6])
            conn.close()
            return share.to_JSON()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_all_share(self):
        try:
            conn = get_connection()
            shares = []
            with conn.cursor() as cur:
                cur.execute(GET_ALL_SHARE)
                resultset = cur.fetchall()
                for row in resultset:
                    share = Share(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                    shares.append(share.to_JSON())
                conn.commit()
            conn.close()
            return shares
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_share(self, share_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DELETE_SHARE,(share_id,))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)