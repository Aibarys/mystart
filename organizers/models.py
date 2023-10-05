from django.db import models
from django.contrib.auth.models import User

class OrganizerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Другие поля для информации об организаторе
