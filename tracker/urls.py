from django.urls import path 
from .views import taskView, taskSpecificView

urlpatterns = [
    path('taskView', taskView, name='taskView'),
    path('taskView/<int:id>"', taskSpecificView, name = "taskSpecificView"),
]