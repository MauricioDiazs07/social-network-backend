from src.database.db import get_connection
from .entities.User import User

class UsersModel():

    @classmethod
    def get_users(self):
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
    def get_user(self, user):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    f""" SELECT full_name, email, usr_password, gender, current_state, municipality, birthday, role_id, level_id FROM T_USER_DATA WHERE email = '{user.email}'
                    """)
                row = cur.fetchone()
                user = User(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7], row[8])
            conn.close()
            return user.to_JSON()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user(self, user):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(
                    """ INSERT INTO T_USER_DATA VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (user.full_name, user.email , user.usr_password, user.gender, user.state, user.municipality, user.birthday, user.role_id))
                affected_row = cur.rowcount
                conn.commit()

            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def login_user(self, user):
        try:
            conn = get_connection()
            authenticated_user = None
            with conn.cursor() as cur:
                cur.execute(
                    """ Select full_name, email, role_id, level_id  from T_USER_DATA where email = %s and usr_password = %s
                    """, (user.email , user.usr_password))
                result = cur.fetchone()
                if result != None:
                    authenticated_user = User(result[0], result[1], None, None, None, None, None, result[2], result[3])
                conn.commit()
            conn.close()
            return authenticated_user
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def test(self):
        try:
            conn = get_connection()

            with conn.cursor() as cur:
                cur.execute("SELECT 1 + 1")
                result = cur.fetchone()
            conn.close()
            return result
        except Exception as ex:
            raise Exception(ex)