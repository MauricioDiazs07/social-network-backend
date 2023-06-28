import datetime
import jwt
import pytz
from decouple import config

class Security():
    
    secret_key = config('JWT_KEY')
    tz = pytz.timezone("America/Mexico_City")

    @classmethod
    def generate_token(self, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=self.tz),
            'exp': datetime.datetime.now(tz=self.tz) + datetime.timedelta(minutes=10),
            'email': authenticated_user.email,
            'fullname': authenticated_user.full_name
        }

        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    @classmethod
    def verify_token(self, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if (len(encoded_token) > 0):
                try:
                    payload = jwt.decode(encoded_token, self.secret_key, algorithms=["HS256"])
                    return True
                except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                    return False

        return False