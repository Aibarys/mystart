from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import OrganizerProfile

@login_required
def register_organizer(request):
    # Регистрация организатора
    pass

@login_required
def manage_marathons(request):
    # Управление марафонами
    pass
