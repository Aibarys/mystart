from django.urls import path
from . import views

urlpatterns = [
    path('marathon/<int:marathon_id>/', views.marathon_stats, name='marathon_stats'),
    path('admin/', views.admin_panel, name='admin_panel'),
]
