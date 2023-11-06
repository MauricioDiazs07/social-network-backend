from src.database.db import get_connection
from src.models.entities.master.Master import Master

DATA = """ SELECT "NAME", "DESCRIPTION", "PROFILE_PHOTO", "EMAIL" FROM "T_PROFILE" WHERE "ID" = %s """


class MasterModel():

    @classmethod
    def get_info(self, profile_id):
        try:
            conn = get_connection()
            with conn.cursor() as cur:
                cur.execute(DATA, (profile_id,))
                row = cur.fetchone()
                master = Master(row[0],row[1],row[2],row[3])
            conn.close()
            master = master.to_JSON()
            master['profile_photo'] = master['profile_photo'][0]
            return master
        except Exception as ex:
            raise Exception(ex)