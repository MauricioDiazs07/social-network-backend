from src.database.db import get_connection
from src.models.entities.multimedia.MultimediaOut import MultimediaOut
from src.models.entities.multimedia.Multimedia import Multimedia

GET_MULTIMEDIA = """ SELECT "ARCHIVE_URL", "ARCHIVE_TYPE" FROM "T_MULTIMEDIA" WHERE "SHARE_ID" = %s """
GET_ALL_MULTIMEDIA = """ SELECT "SHARE_ID", "SHARE_TYPE", "ARCHIVE_URL", "ARCHIVE_TYPE" FROM "T_MULTIMEDIA" """
DELETE_MULTIMEDIA = """ DELETE FROM "T_MULTIMEDIA" WHERE "SHARE_ID" = %s """
CREATE_MULTIMEDIA = """ INSERT INTO "T_MULTIMEDIA" ("SHARE_ID","SHARE_TYPE","ARCHIVE_URL","ARCHIVE_TYPE") VALUES (%s,%s,%s,%s) """

class MultimediaModel():

    @classmethod
    def get_multimedia(self, id):
        try:
            conn = get_connection()
            multimedia_list = []
            with conn.cursor() as cur:
                cur.execute(GET_MULTIMEDIA, (id,))
                resultset = cur.fetchall()
                for row in resultset:
                    multimedia = MultimediaOut(row[0],row[1])
                    multimedia_list.append(multimedia.to_JSON())
            return multimedia_list
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_all_multimedia(self):
        try:
            conn = get_connection()
            multimedia_list = []
            with conn.cursor() as cur:
                cur.execute(GET_ALL_MULTIMEDIA)
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
    def delete_multimedia(self, share_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DELETE_MULTIMEDIA,(share_id,))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)