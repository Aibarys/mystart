from django.urls import path
from . import views
from django.views.defaults import page_not_found



app_name = 'marathons'

urlpatterns = [
    path('', views.marathon_list, name='marathon_list'),
    path('create/', views.create_marathon, name='create_marathon'),
    path('register/<int:marathon_id>/', views.register_for_marathon, name='register_for_marathon'),
    path('<slug:marathon>', views.marathon_detail, name='marathon_detail'),
]

handler404 = 'marathons.views.custom_404_view'