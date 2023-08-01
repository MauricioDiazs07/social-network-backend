from src.database.db import get_connection
from .entities.share.Share import Share
from .entities.share.Multimedia import Multimedia


CREATE_SHARE = """ INSERT INTO "T_SHARE" ("PROFILE_ID", "SHARE_TYPE", "DESCRIPTION") VALUES (%s, %s, %s) RETURNING "ID" """
CREATE_MULTIMEDIA = """ INSERT INTO "T_MULTIMEDIA" ("SHARE_ID","SHARE_TYPE","ARCHIVE_URL","ARCHIVE_TYPE") VALUES (%s,%s,%s,%s) """
GET_SHARE = """ SELECT "ID", "PROFILE_ID", "SHARE_TYPE", "DESCRIPTION" FROM "T_SHARE" WHERE "ID" = %s """
GET_MULTIMEDIA = """ SELECT "SHARE_ID", "SHARE_TYPE", "ARCHIVE_URL", "ARCHIVE_TYPE" FROM "T_MULTIMEDIA" WHERE "SHARE_ID" = %s """
GET_ALL_SHARE = """ SELECT "ID", "PROFILE_ID", "SHARE_TYPE", "DESCRIPTION" FROM "T_SHARE" """
DELETE_SHARE = """ delete from "T_SHARE" where "ID" = %s """
DELETE_MULTIMEDIA = """ delete from "T_MULTIMEDIA" where "SHARE_ID" = %s """

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
                share = Share(result[0],result[1],result[2], result[3])
            conn.close()
            return share.to_JSON()
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def get_multimedia(self, id):
        try:
            conn = get_connection()
            multimedia_list = []
            with conn.cursor() as cur:
                cur.execute(GET_MULTIMEDIA, (id,))
                resultset = cur.fetchall()
                for row in resultset:
                    multimedia = Multimedia(row[0],row[1],row[2],row[3])
                    multimedia_list.append(multimedia.to_JSON())
            return multimedia_list
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def create_multimedia(self, multimedia):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(CREATE_MULTIMEDIA, (multimedia.share_id, multimedia.share_type, multimedia.archive_url, multimedia.archive_type))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_all(self):
        try:
            conn = get_connection()
            shares = []
            with conn.cursor() as cur:
                cur.execute(GET_ALL_SHARE)
                resultset = cur.fetchall()
                for row in resultset:
                    share = Share(row[0],row[1],row[2], row[3])
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
                cur.execute(DELETE_MULTIMEDIA,(share_id,))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)