from django import forms
from .models import MarathonDistance, Marathon, Distance

class MarathonDistanceForm(forms.ModelForm):
    class Meta:
        model = MarathonDistance
        fields = ['distance', 'price']

    # Дополнительные настройки формы (необязательно)
    widgets = {
        'distance': forms.TextInput(attrs={'class': 'form-control'}),
        'price': forms.TextInput(attrs={'class': 'form-control'}),
    }
    
class DistancePriceForm(forms.Form):
    distance = forms.ModelChoiceField(queryset=Distance.objects.all(), widget=forms.Select(attrs={'class': 'select-box'}))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'price-input'}))
    
class MarathonForm(forms.ModelForm):
    
    distances_and_prices = forms.formset_factory(DistancePriceForm, extra=1)
    class Meta:
        model = Marathon
        fields = ['title', 'description', 'poster', 'start_location', 'date_and_time', 'max_participants', 'file_attachment']


class SearchForm(forms.Form):
    query = forms.CharField()