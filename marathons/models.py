from django.db import models
from django.core.validators import FileExtensionValidator
from users.models import UserProfile
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status=Marathon.Status.PUBLISHED)
    

class Distance(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Marathon(models.Model):
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
        
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ImageField(upload_to='marathon_posters', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    start_location = models.CharField(max_length=255)
    date_and_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    file_attachment = models.FileField(upload_to='marathon_attachments', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg'])])
    distances = models.ManyToManyField(Distance, through='MarathonDistance')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author', verbose_name='Автор', default=1)
    publish = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=250, unique_for_date='publish', blank=True)
    objects = models.Manager() # менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер
    participants = models.ManyToManyField(UserProfile, through='Participation', related_name='marathons_participated')

    
    def save(self, *args, **kwargs):
        if not self.slug:
            # начните с преобразования title в slug
            self.slug = slugify(self.title)
            
            # если slug уже существует, добавьте к нему номер
            orig_slug = self.slug
            counter = 1
            while Marathon.objects.filter(slug=self.slug).exists():
                self.slug = f"{orig_slug}-{counter}"
                counter += 1
        
        super(Marathon, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

        verbose_name = 'Марафон'
        verbose_name_plural = 'Марафоны'
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('marathons:marathon_detail', args=[self.slug])
    

class MarathonDistance(models.Model):
    marathon = models.ForeignKey(Marathon, on_delete=models.CASCADE)
    distance = models.ForeignKey(Distance, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marathon.title} - {self.distance.name} ({self.price} тнг.)"

class Participation(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    marathon = models.ForeignKey(Marathon, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)  # Дата и время, когда пользователь присоединился к марафону

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.marathon.title}"

