from src.database.db import get_connection
from src.models.entities.chat.InfoChat import InfoChat
from src.models.entities.chat.ShowChats import ShowChats

INSERT_CHAT = """ INSERT INTO "T_CHAT" ("SENDER_ID","RECEIVER_ID","TEXT") VALUES (%s,%s,%s) """
LIST_CHAT = """ 
SELECT "SENDER_ID","TEXT","NAME","PROFILE_PHOTO","T_CHAT"."CREATION_DATE" FROM "T_CHAT" 
INNER JOIN "T_PROFILE" ON
"T_PROFILE"."ID" = "T_CHAT"."SENDER_ID" 
WHERE ("SENDER_ID" = %s AND "RECEIVER_ID" = %s) 
OR ("SENDER_ID" = %s AND "RECEIVER_ID" = %s)
ORDER BY "T_CHAT"."CREATION_DATE" ASC;
 """

SHOW_CHATS = """
SELECT "NAME","SENDER_ID","RECEIVER_ID","TEXT","T_CHAT"."CREATION_DATE","PROFILE_PHOTO" FROM "T_CHAT" 
INNER JOIN "T_PROFILE" ON
"T_PROFILE"."ID" = "T_CHAT"."SENDER_ID" 
WHERE "SENDER_ID" = %s OR "RECEIVER_ID" = %s
ORDER BY "T_CHAT"."CREATION_DATE" DESC;

"""

class ChatModel:

    @classmethod
    def create_chat(self, chat):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute( INSERT_CHAT, (chat.sender_id,chat.receiver_id,chat.text))
                affected_row = cur.rowcount
                conn.commit()
            conn.close()
            return affected_row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def list_chats(self, sender_id, receiver_id):
        try:
            conn = get_connection()
            chats = []
            with conn.cursor() as cur:
                cur.execute( LIST_CHAT, (sender_id,receiver_id,receiver_id,sender_id))
                resultset = cur.fetchall()
                for row in resultset:
                    chat = InfoChat(row[0],row[1],row[2],row[3],row[4], sender_id).to_JSON()
                    chats.append(chat)
            conn.close()
            return chats
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def show_chats(self, sender_id):
        try:
            conn = get_connection()
            chats = []
            with conn.cursor() as cur:
                cur.execute( SHOW_CHATS, (sender_id,sender_id))
                resultset = cur.fetchall()
                for row in resultset:
                    chat = ShowChats(row[0],row[1],row[2],row[3],row[4],row[5]).to_JSON()
                    chats.append(chat)
            conn.close()
            return chats
        except Exception as ex:
            raise Exception(ex)