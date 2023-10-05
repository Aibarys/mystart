from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_organizer, name='register_organizer'),
    path('manage_marathons/', views.manage_marathons, name='manage_marathons'),
]
