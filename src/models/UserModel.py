from src.database.db import get_connection
from .entities.user.User import User

GET_USER_DATA = """ SELECT "NAME", "BIRTHDATE", "GENDER", "STATE", "MUNICIPALITY", "EMAIL", "PHONE_NUMBER", "PROFILE_PHOTO" FROM "T_USER_DATA" JOIN "T_PROFILE" ON "T_USER_DATA"."PROFILE_ID" = "T_PROFILE"."ID" WHERE "T_PROFILE"."ID" = %s """
UPDATE = ""

class UsersModel():

    @classmethod
    def update_user(self):
        try:
            conn = get_connection()
            users = []
            with conn.cursor() as cur:
                cur.execute("SELECT full_name, email, usr_password, gender, current_state, municipality, birthday, role_id, level_id FROM T_USER_DATA ORDER BY full_name ASC")
                resultset = cur.fetchall()

                for row in resultset:
                    user = User(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])
                    users.append(user.to_JSON())

            conn.close()
            return users
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
    