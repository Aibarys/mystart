from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    first_name = models.CharField(max_length=30, validators=[
        RegexValidator(
            regex='^[a-zA-Z ]+$',  # Разрешаем только латинские буквы и пробелы
            message='Имя может содержать только латинские буквы и пробелы.',
        ),
    ])

    # Поле last_name (на латинице только)
    last_name = models.CharField(max_length=30, validators=[
        RegexValidator(
            regex='^[a-zA-Z ]+$',  # Разрешаем только латинские буквы и пробелы
            message='Фамилия может содержать только латинские буквы и пробелы.',
        ),
    ])

    # Поле емейла
    email = models.EmailField()

    # Пол (выборка из мужской/женский/другой)
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('other', 'Другой'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # Номер телефона
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Город
    city = models.CharField(max_length=255, blank=True)

    # Размер футболки (выборка из XS, S, M, L, XL, XXL)
    SHIRT_SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    ]
    shirt_size = models.CharField(max_length=4, choices=SHIRT_SIZE_CHOICES, blank=True)

    # Социальные сети
    social_media = models.CharField(max_length=255, blank=True)

    # Сфера деятельности
    occupation = models.CharField(max_length=255, blank=True)

    # Беговой клуб
    running_club = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username