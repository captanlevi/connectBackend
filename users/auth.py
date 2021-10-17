from django.core.exceptions import ObjectDoesNotExist
import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .models import User



class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        # Return the failure reason instead of an HttpResponse
        return reason


class SafeJWTAuthentication(BaseAuthentication):
    '''
        custom authentication class for DRF and JWT
        https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    '''

    def authenticate(self, request):

        authorizationHeader = request.headers.get('Authorization')

        if not authorizationHeader:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            accessToken = authorizationHeader.split(' ')[1]
            payload = jwt.decode(
                accessToken, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('accessToken expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Token not valid")


        try:
            user = User.objects.get(id = payload["userId"])
        except ObjectDoesNotExist:
            raise exceptions.AuthenticationFailed("User does not exist")
     
        #if not user.is_active:
        #    raise exceptions.AuthenticationFailed('user is inactive')

        #self.enforce_csrf(request)     #-------------- DISABLED CSFR FOR TESTING
        return (user, None)

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck()
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)