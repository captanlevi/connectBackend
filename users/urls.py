from django.urls import path , include
from .views import loginView, logoutView, refreshTokenView, isLoggedIn, registerView, test

urlpatterns = [
    path('login', loginView, name='login'),
    path('logout', logoutView, name = "logout"),
    path('refreshToken', refreshTokenView, name = "refreshToken"),
    path('isLoggedIn', isLoggedIn , name = "isLoggedIn"),
    path('signUp', registerView, name = "signUp"),
    path('test', test, name = "test"),

]