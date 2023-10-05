from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import UserProfile

class Marathon(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ImageField(upload_to='marathon_posters', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    start_location = models.CharField(max_length=255)
    date_and_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    file_attachment = models.FileField(upload_to='marathon_attachments', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])
    distances = models.ManyToManyField('Distance', through='MarathonDistance')

    def __str__(self):
        return self.title

class Distance(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MarathonDistance(models.Model):
    marathon = models.ForeignKey(Marathon, on_delete=models.CASCADE)
    distance = models.ForeignKey(Distance, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marathon.title} - {self.distance.name} ({self.price} руб.)"

class Participant(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    marathon = models.ForeignKey(Marathon, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.marathon.title}"
