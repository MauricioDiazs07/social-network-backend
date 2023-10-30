from src.database.db import get_connection
from .entities.user.User import User

GET_USER_DATA = """ SELECT "NAME", "BIRTHDATE", "GENDER", "STATE", "MUNICIPALITY", "EMAIL", "PHONE_NUMBER", "PROFILE_PHOTO" FROM "T_USER_DATA" JOIN "T_PROFILE" ON "T_USER_DATA"."PROFILE_ID" = "T_PROFILE"."ID" WHERE "T_PROFILE"."ID" = %s """
UPDATE_PHOTO = """ UPDATE "T_PROFILE" SET "EMAIL"= %s, "PHONE_NUMBER" = %s, "PROFILE_PHOTO" = %s WHERE  "ID" = %s; """
UPDATE = """ UPDATE "T_PROFILE" SET "EMAIL"= %s, "PHONE_NUMBER" = %s WHERE  "ID" = %s; """
GET_ID = """ SELECT "ID" FROM "T_PROFILE" WHERE "PHONE_NUMBER" = %s """
UPDATE_PASSWORD = """ UPDATE "T_PROFILE" SET "PASSWORD" = %s WHERE "ID" = %s """

DELETE_PROFILE = """ DELETE FROM "T_PROFILE" WHERE "ID" = %s """
DELETE_USER = """ DELETE FROM "T_USER_DATA" WHERE "PROFILE_ID" = %s """
DELETE_INTEREST = """ DELETE FROM "T_USER_INTEREST" WHERE "PROFILE_ID"  = %s """
DELETE_LIKE = """ DELETE FROM "T_INTERACTION_LIKE" WHERE "PROFILE_ID"  = %s """
DELETE_COMMENT = """ DELETE FROM "T_INTERACTION_COMMENT" WHERE "PROFILE_ID"  = %s """
DELETE_SHARE = """ DELETE FROM "T_SHARE"  WHERE "PROFILE_ID"  = %s """

class UsersModel():

    @classmethod
    def update_user(self, profile_id, email, phone_number):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE, (email,phone_number,profile_id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def update_data_photo_user(self, profile_id, email, phone_number,profile_photo):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE_PHOTO, (email,phone_number,profile_photo,profile_id))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user_data(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(GET_USER_DATA, (profile_id,))
                row = cur.fetchone()
                user = User(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            conn.close()
            return user.to_JSON()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_id_by_phone(self, phone):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(GET_ID, (phone,))
                row = cur.fetchone()
            conn.close()
            return row
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def delete_user_data(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DELETE_USER, (profile_id,))
                cur.execute(DELETE_INTEREST, (profile_id,))
                cur.execute(DELETE_LIKE, (profile_id,))
                cur.execute(DELETE_COMMENT, (profile_id,))
                cur.execute(DELETE_SHARE, (profile_id,))
                cur.execute(DELETE_PROFILE, (profile_id,))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def update_password(self, password, profileId):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(UPDATE_PASSWORD, (password,profileId))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)