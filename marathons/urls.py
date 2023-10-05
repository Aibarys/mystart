from django.urls import path
from . import views

urlpatterns = [
    path('marathons/', views.marathon_list, name='marathon_list'),
    path('create/', views.create_marathon, name='create_marathon'),
    path('register/<int:marathon_id>/', views.register_for_marathon, name='register_for_marathon'),
    path('<int:marathon_id>/', views.marathon_detail, name='marathon_detail'),
]
