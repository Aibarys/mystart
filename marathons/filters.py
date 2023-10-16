import django_filters
from .models import Marathon

class MarathonFilter(django_filters.FilterSet):
    class Meta:
        model = Marathon
        fields = ['date_and_time', 'start_location', 'distances']