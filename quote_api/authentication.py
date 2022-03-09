import datetime
import jwt
from django.conf import settings

def generate_access_token(user):
    info = {
      "user_id": user.id,
      #expiration time
      "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      #started at time
      "iat": datetime.datetime.utcnow(),
    }

    #encode using the secrete key
    return jwt.encode(info, settings.SECRET_KEY, algorithm="HS256")
