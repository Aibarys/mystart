from django.shortcuts import render
from marathons.models import Marathon
from .models import MarathonStats

def marathon_stats(request, marathon_id):
    marathon = Marathon.objects.get(id=marathon_id)
    stats = MarathonStats.objects.filter(marathon=marathon)
    # Ваш код для отображения статистики
    return render(request, 'dashboard/marathon_stats.html', {'marathon': marathon, 'stats': stats})

def admin_panel(request):
    # Ваш код для административной панели
    return render(request, 'dashboard/admin_panel.html')
