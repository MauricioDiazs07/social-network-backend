from src.database.db import get_connection


CREATE_SHARE = """ INSERT INTO "T_SHARE" ("PROFILE_ID", "SHARE_TYPE", "DESCRIPTION") VALUES (%s, %s, %s) RETURNING "ID" """
CREATE_MULTIMEDIA = """ INSERT INTO "T_MULTIMEDIA" ("SHARE_ID","SHARE_TYPE","ARCHIVE_URL","ARCHIVE_TYPE") VALUES (%s,%s,%s,%s) """

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