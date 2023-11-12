from src.database.db import get_connection
from src.models.entities.interaction.ReadComment import ReadComment
from src.models.entities.interaction.ReadLike import ReadLike;

CREATE_COMMENT = """ INSERT INTO "T_INTERACTION_COMMENT" ("PROFILE_ID","SHARE_ID","SHARE_TYPE","TEXT","FEELING_ID","FEELING_PERCENTAGE") VALUES (%s,%s,%s,%s,%s,%s) """
READ_ALL_COMMENTS = """ SELECT "T_INTERACTION_COMMENT"."ID","NAME","PROFILE_ID","T_PROFILE"."PROFILE_PHOTO","T_INTERACTION_COMMENT"."TEXT","SHARE_ID","SHARE_TYPE","T_INTERACTION_COMMENT"."CREATION_DATE"  FROM "T_INTERACTION_COMMENT"  INNER JOIN "T_PROFILE" ON "T_INTERACTION_COMMENT"."PROFILE_ID" = "T_PROFILE"."ID" ORDER BY "T_INTERACTION_COMMENT"."CREATION_DATE" ASC """
READ_COMMENT = """ SELECT "T_INTERACTION_COMMENT"."ID","NAME","PROFILE_ID","T_PROFILE"."PROFILE_PHOTO","T_INTERACTION_COMMENT"."TEXT","SHARE_ID","SHARE_TYPE","T_INTERACTION_COMMENT"."CREATION_DATE"  FROM "T_INTERACTION_COMMENT"  INNER JOIN "T_PROFILE" ON "T_INTERACTION_COMMENT"."PROFILE_ID" = "T_PROFILE"."ID" WHERE "SHARE_ID" = %s """
UPDATE_COMMENT = """ UPDATE "T_INTERACTION_COMMENT" SET "TEXT" = %s WHERE "ID" = %s """
DELETE_COMMENT = """ DELETE FROM "T_INTERACTION_COMMENT" WHERE "ID" = %s """
DELETE_ALL_COMMENTS = """ DELETE FROM "T_INTERACTION_COMMENT" WHERE "SHARE_ID" = %s """

ADD_LIKE = """ INSERT INTO "T_INTERACTION_LIKE" ("PROFILE_ID","SHARE_ID","SHARE_TYPE") VALUES (%s,%s,%s) """
COUNT_LIKE = """ SELECT COUNT(*) AS "LIKES" FROM "T_INTERACTION_LIKE" WHERE "SHARE_ID" = %s """
GET_LIKES = """ SELECT "T_INTERACTION_LIKE"."PROFILE_ID", "NAME", "PROFILE_PHOTO", "SHARE_ID", "SHARE_TYPE" FROM "T_INTERACTION_LIKE" INNER JOIN "T_PROFILE" ON "T_INTERACTION_LIKE"."PROFILE_ID" = "T_PROFILE"."ID" WHERE "SHARE_ID" = %s  """
GET_ALL_LIKES = """ SELECT "T_INTERACTION_LIKE"."PROFILE_ID", "NAME", "PROFILE_PHOTO", "SHARE_ID", "SHARE_TYPE" FROM "T_INTERACTION_LIKE" INNER JOIN "T_PROFILE" ON "T_INTERACTION_LIKE"."PROFILE_ID" = "T_PROFILE"."ID" """
REMOVE_LIKE = """ DELETE FROM "T_INTERACTION_LIKE" WHERE "PROFILE_ID" = %s AND "SHARE_ID" = %s AND "SHARE_TYPE" = %s """
DELETE_ALL_LIKES = """ DELETE FROM "T_INTERACTION_LIKE" WHERE "SHARE_ID" = %s """

class InteractionModel():

    @classmethod
    def create_comment(self, comment):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(CREATE_COMMENT, (comment.profile_id, comment.share_id,comment.share_type,comment.text, comment.feeling_id, comment.feeling_percentage))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_comment(self,id,comment):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE_COMMENT, (comment, id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_comment(self, id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DELETE_COMMENT, (id,))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_all_comments(self, share_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DELETE_ALL_COMMENTS, (share_id,))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def delete_all_likes(self, share_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DELETE_ALL_LIKES, (share_id,))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_all_comments(self):
        try:
            conn = get_connection()
            comments = []
            with conn.cursor() as cur:
                cur.execute(READ_ALL_COMMENTS)
                resultset = cur.fetchall()
                for row in resultset:
                    comment = ReadComment(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                    comments.append(comment.to_JSON())
            conn.close()
            return comments
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_comment(self, id):
        try:
            conn = get_connection()
            comments = []
            with conn.cursor() as cur:
                cur.execute(READ_COMMENT, (id,))
                resultset = cur.fetchall()
                for row in resultset:
                    comment = ReadComment(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]).to_JSON()
                    comment.pop('share_id')
                    comment.pop('share_type')
                    comments.append(comment)
            return comments
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def add_like(self, like):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(ADD_LIKE, (like.profile_id, like.share_id,like.share_type))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def dislike(self, like):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(REMOVE_LIKE, (like.profile_id, like.share_id,like.share_type))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def count_likes(self, id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(COUNT_LIKE, (id,))
                result = cur.fetchone()
            conn.close()
            return result[0]
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_likes(self, id):
        try:
            conn = get_connection()
            likes = []
            with conn.cursor() as cur:
                cur.execute(GET_LIKES, (id,))
                resultset = cur.fetchall()
                for row in resultset:
                    like = ReadLike(row[0],row[1],row[2],row[3],row[4]).to_JSON()
                    like.pop('share_id')
                    like.pop('share_type')
                    likes.append(like)
            conn.close()
            return likes
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_all_likes(self):
        try:
            conn = get_connection()
            likes = []
            with conn.cursor() as cur:
                cur.execute(GET_ALL_LIKES)
                resultset = cur.fetchall()
                for row in resultset:
                    like = ReadLike(row[0],row[1],row[2],row[3],row[4])
                    likes.append(like.to_JSON())
            conn.close()
            return likes
        except Exception as ex:
            raise Exception(ex)