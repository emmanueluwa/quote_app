import datetime
import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User

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

#responsible for authenticating the user
class JWTAuthentication(BaseAuthentication):
    #read cookie in users browser, validate it exists in db
    def authenticate(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            #the secret key used to encode is used to decode the token
            info = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("authentication failed")

        #if the token was decoded then get the user
        user = get_object_or_404(User, id=info["user_id"])

        return(user, None)
