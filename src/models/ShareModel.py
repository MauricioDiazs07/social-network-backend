from src.database.db import get_connection
from src.models.entities.share.Share import Share


CREATE_SHARE = """ INSERT INTO "T_SHARE" ("PROFILE_ID", "SHARE_TYPE", "DESCRIPTION") VALUES (%s, %s, %s) RETURNING "ID" """
GET_ALL_SHARE = """ SELECT "T_SHARE"."ID","NAME","PROFILE_ID","T_PROFILE"."PROFILE_PHOTO","T_SHARE"."DESCRIPTION","SHARE_TYPE","T_SHARE"."CREATION_DATE" FROM "T_SHARE"  INNER JOIN "T_PROFILE" ON "T_SHARE"."PROFILE_ID" = "T_PROFILE"."ID" ORDER BY "T_SHARE"."CREATION_DATE" ASC """
GET_SHARE = """ SELECT "T_SHARE"."ID","NAME","PROFILE_ID","T_PROFILE"."PROFILE_PHOTO","T_SHARE"."DESCRIPTION","SHARE_TYPE","T_SHARE"."CREATION_DATE" FROM "T_SHARE"  INNER JOIN "T_PROFILE" ON "T_SHARE"."PROFILE_ID" = "T_PROFILE"."ID" WHERE "T_SHARE"."ID" = %s """
DELETE_SHARE = """ delete from "T_SHARE" where "ID" = %s """
UPDATE_SHARE = """ UPDATE "T_SHARE" SET "DESCRIPTION" = %s WHERE "ID" = %s """
GET_SHARE_FROM_PROFILE = """ SELECT "T_SHARE"."ID","NAME","PROFILE_ID","T_PROFILE"."PROFILE_PHOTO","T_SHARE"."DESCRIPTION","SHARE_TYPE","T_SHARE"."CREATION_DATE" FROM "T_SHARE"  INNER JOIN "T_PROFILE" ON "T_SHARE"."PROFILE_ID" = "T_PROFILE"."ID" WHERE "T_PROFILE"."ID" = %s ORDER BY "T_SHARE"."CREATION_DATE" ASC;  """

GET_SHARE_FROM_INTEREST = """ SELECT "SHARE_ID","NAME","PROFILE_ID","PROFILE_PHOTO","T_SHARE"."DESCRIPTION","SHARE_TYPE","T_SHARE"."CREATION_DATE" FROM "T_SHARE" 
INNER JOIN "T_PROFILE" ON "T_SHARE"."PROFILE_ID" = "T_PROFILE"."ID"
INNER JOIN "T_SHARE_INTEREST" ON "T_SHARE"."ID" = "T_SHARE_INTEREST"."SHARE_ID" 
WHERE "INTEREST_ID" = %s AND "SHARE_TYPE" = 'POST' ORDER BY RANDOM() LIMIT %s"""

GET_SHARE_FROM_INTEREST_FILTER = """ SELECT "SHARE_ID","NAME","PROFILE_ID","PROFILE_PHOTO","T_SHARE"."DESCRIPTION","SHARE_TYPE","T_SHARE"."CREATION_DATE" FROM "T_SHARE" 
INNER JOIN "T_PROFILE" ON "T_SHARE"."PROFILE_ID" = "T_PROFILE"."ID"
INNER JOIN "T_SHARE_INTEREST" ON "T_SHARE"."ID" = "T_SHARE_INTEREST"."SHARE_ID" 
WHERE "INTEREST_ID" = %s AND "SHARE_TYPE" = 'POST' AND "SHARE_ID" NOT IN %s ORDER BY RANDOM() LIMIT %s"""


class ShareModel():

    @classmethod
    def get_share_from_interest(self,interest_id, page_size):
        try:
            conn = get_connection()
            shares = []
            with conn.cursor() as cur:
                cur.execute(GET_SHARE_FROM_INTEREST,(interest_id,page_size))
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
    def get_share_from_interest_filter(self,interest_id, post_history, page_size):
        try:
            conn = get_connection()
            shares = []
            with conn.cursor() as cur:
                cur.execute(GET_SHARE_FROM_INTEREST_FILTER,(interest_id,tuple(post_history),page_size))
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
    def update_share(self, id, description):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE_SHARE, (description, id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
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
                    return None
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
    def get_shares_from_profile(self, profile_id):
        try:
            conn = get_connection()
            shares = []
            with conn.cursor() as cur:
                cur.execute(GET_SHARE_FROM_PROFILE, (profile_id,))
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