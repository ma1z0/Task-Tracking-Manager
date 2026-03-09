from django.urls import path

from . import views

urlpatterns = [
    path("", views.tasks_list),
    path("<int:pk>/", views.task_detail),
]