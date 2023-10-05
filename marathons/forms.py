from django import forms
from .models import MarathonDistance, Marathon

class MarathonDistanceForm(forms.ModelForm):
    class Meta:
        model = MarathonDistance
        fields = ['distance', 'price']

    # Дополнительные настройки формы (необязательно)
    widgets = {
        'distance': forms.TextInput(attrs={'class': 'form-control'}),
        'price': forms.TextInput(attrs={'class': 'form-control'}),
    }
    
    
class MarathonForm(forms.ModelForm):
    class Meta:
        model = Marathon
        fields = ['title', 'description', 'poster', 'start_location', 'date_and_time', 'max_participants', 'file_attachment']
