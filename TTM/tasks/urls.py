from django.urls import path

from . import views

urlpatterns = [
    path("", views.tasks_list),
]