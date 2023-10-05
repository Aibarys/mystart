from django.db import models
from marathons.models import Marathon

class MarathonStats(models.Model):
    marathon = models.ForeignKey(Marathon, on_delete=models.CASCADE)
    # Другие поля для статистики, например, количество участников, результаты и т.д.
