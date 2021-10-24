from .models import User
import datetime 
import jwt
from django.conf import settings
from django.core.exceptions import ValidationError
import requests
from rest_framework import exceptions
from django.core.exceptions import ObjectDoesNotExist
from connectBackend.settings import GOOGLE_VERIFICATION_URL
from .models import User

def generateAccessToken(user):

    accessTokenPayload = {
        'userId' : user.id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=100),  # 100 mins for testing replace it by 5 in prod
        'iat': datetime.datetime.utcnow()
    }

    accessToken = jwt.encode(payload = accessTokenPayload , key = settings.SECRET_KEY, algorithm= 'HS256' )

    return accessToken

def generateRefreshToken(user, token_version = None):
    refreshTokenPayload = {
        'userId': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    refreshToken = jwt.encode(
        refreshTokenPayload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')

    return refreshToken





def verifyGoogleAccessCode(tokenId : str) -> User:
    url = GOOGLE_VERIFICATION_URL + tokenId
    res = requests.get(url)
    if(res.status_code != 200):
        raise exceptions.AuthenticationFailed("Google account is invalid")
    
    verified_dict = res.json()
    if not verified_dict:
        raise exceptions.AuthenticationFailed("Google account is invalid")

    is_verified = verified_dict.get("email_verified")
    if not is_verified:
        raise exceptions.AuthenticationFailed("Google account is not verified")

    emailId = verified_dict.get("email")
    
    return emailId