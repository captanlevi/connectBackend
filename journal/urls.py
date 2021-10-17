from django.urls import path
from .views import *

urlpatterns = [
    path("journalView", journalView),
    path("journalView/<int:id>", journalViewByID)
]
