from django import forms
from .models import UserProfile, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']
        
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # Укажите модель, для которой создается форма
        fields = ['first_name', 'last_name', 'email', 'gender', 'phone_number', 'city', 'shirt_size', 'social_media', 'occupation', 'running_club']
        # Укажите поля профиля, которые вы хотите редактировать