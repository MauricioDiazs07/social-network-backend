from src.database.db import get_connection
from src.models.entities.master.Master import Master

DATA = """ SELECT "NAME", "DESCRIPTION", "PROFILE_PHOTO" FROM "T_PROFILE" WHERE "ID" = %s """


class MasterModel():

    @classmethod
    def get_info(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DATA, (profile_id,))
                row = cur.fetchone()
                master = Master(row[0],row[1],row[2])
            conn.close()
            return master.to_JSON()
        except Exception as ex:
            raise Exception(ex)