from django.contrib import admin
from .models import Marathon, Distance, MarathonDistance

class MarathonDistanceInline(admin.TabularInline):
    model = MarathonDistance
    extra = 1  # Указывает количество пустых форм для добавления

@admin.register(Marathon)
class MarathonAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_and_time', 'max_participants', 'slug', 'get_distance_and_price']
    list_filter = ['date_and_time', 'status', 'publish', 'author']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    search_fields = ['title']
    
    def get_distance_and_price(self, obj):
        distances_and_prices = []
        for marathon_distance in obj.marathondistance_set.all():
            distances_and_prices.append(f"{marathon_distance.distance.name} ({marathon_distance.price} тнг.)")
        return ", ".join(distances_and_prices)
    
    get_distance_and_price.short_description = 'Дистанции и цены'
    
    inlines = [MarathonDistanceInline]

@admin.register(Distance)
class DistanceAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(MarathonDistance)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['marathon', 'distance', 'price']
