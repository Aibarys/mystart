from django.contrib import admin
from .models import Marathon, Distance, MarathonDistance
@admin.register(Marathon)
class RunningEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_distances', 'author', 'date_and_time', 'max_participants', 'slug']
    list_filter = ['date_and_time', 'status', 'publish', 'author']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    search_fields = ['title']
    
    def get_distances(self, obj):
        return ", ".join([distance.name for distance in obj.distances.all()])
    
    get_distances.short_description = 'Дистанции'
    

    
    
@admin.register(Distance)
class DistanceAdmin(admin.ModelAdmin):
    list_display = ['name']
    
@admin.register(MarathonDistance)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['marathon', 'distance', 'price']