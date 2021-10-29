from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import rest_framework
from .serializers import UserSerializer
# Create your views here.
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model  # I have made a custom User model , as recommended in the django docs
from rest_framework.response import Response
from rest_framework import exceptions ,status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes , authentication_classes
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect, csrf_exempt
from .serializers import UserSerializer
from .utils import generateAccessToken, generateRefreshToken, verifyGoogleAccessCode
from django.conf import settings
import jwt


"""
1) DRF disable CSRF protection for all the APIView.
2) Login end point is open to all , and we will send a csfr cookie if login is successful
    request data must have "email" and "password" (google and facebook login comming soon)
    Gives out accessToken(in .data) and refreshToken(httponly cookie) and csfr token(cookie) if successful
3) refrestToken end point is open to all , 2 conditions are to be met
        The refresh token is valid
        The csfr token is valid 
    Gives out a accessToken(valid for a short time), or errors if refreshToken is expired or other errors,
    requires clients to set the 'X-CSRFTOKEN' IN THE header    
"""




@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def registerView(request :rest_framework.request.Request ):
    authorizationHeader = request.headers.get('Authorization')
    if not authorizationHeader:
        raise exceptions.AuthenticationFailed("Must provide google access key id in the authorizationHeader")
    

    tokenId = authorizationHeader.split()[1]
    email_id :str =  verifyGoogleAccessCode(tokenId)


    try:
        user = User.objects.get(email = email_id)
        return Response(UserSerializer(user).data)
    except ObjectDoesNotExist:
        user_data = request.data
        user_data["email"] = email_id
        serializer = UserSerializer(data = user_data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def loginView(request : rest_framework.request.Request):
    """
    password = request.data.get("password")
    
    if(email is None) or (password is None):
        raise exceptions.AuthenticationFailed("email and password required")
    user = User.objects.filter(email = email).first()
    if(user is None):
        raise exceptions.AuthenticationFailed("user not found")
    if(not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')
    """
    # WiLL implement a logic that gets a google access token and the logs the user in
    authorizationHeader = request.headers.get('Authorization')
    if not authorizationHeader:
        raise exceptions.AuthenticationFailed("Must provide google access key id in the authorizationHeader")

    tokenId = authorizationHeader.split()[1]

    """
    During dev time you can set the user manually , so that you may not need 
    front end and can test on postman
    user =  User.objects.all()[0]
    """

    email_id :str =  verifyGoogleAccessCode(tokenId)

    try:
        user = User.objects.get(email = email_id)
    except ObjectDoesNotExist:
        raise exceptions.AuthenticationFailed("User does not exists, please sign up first")




    res = Response()
    """
    try:
        user = User.objects.get(email = email)
    except ObjectDoesNotExist:
        raise exceptions.AuthenticationFailed("This email is not registered")
    """
    serializedUser = UserSerializer(user).data

    accessToken = generateAccessToken(user)
    refrestToken = generateRefreshToken(user)



    res.data = {
        'accessToken' : accessToken,
        'user' : serializedUser

    }
    res.set_cookie(key = "refreshToken", value= refrestToken, httponly= True)
    res.set_cookie(key = "testCookie" , value = "HELLO WORLD")


    return res


@api_view(["POST"])
@csrf_protect
def isLoggedIn(request):
    if(request.method == "POST"):
        return Response(True)







@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_protect
def refreshTokenView(request):
    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''
    User = get_user_model()
    refreshToken = request.COOKIES.get('refreshToken')
    print("got refrest token")
    if refreshToken is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refreshToken, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('userId')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

#    if not user.is_active:
#        raise exceptions.AuthenticationFailed('user is inactive')


    accessToken = generateAccessToken(user)
    return Response({'accessToken': accessToken})



@api_view(["POST"])
def logoutView(request):
    res = Response()
    res.delete_cookie("refreshToken")
    res.delete_cookie("csrftoken")
    """
    Apart for deleting the cookies , we also need to mark the accessToken as blacklisted till the expiration time
    """
    return res


@api_view(["GET"])
def test(request):
    all_objects = User.objects.all()
    serializer = UserSerializer(instance= all_objects, many = True)
    return Response(serializer.data)
