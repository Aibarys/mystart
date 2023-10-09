from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Marathon, Participant, MarathonDistance
from .forms import MarathonDistanceForm, MarathonForm, Marathon
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def marathon_list(request):
    marathon_list = Marathon.published.all()
    marathonDistance = MarathonDistance.objects.all()
    paginator = Paginator(marathon_list, 6) 
    page_number = request.GET.get('page', 1)
    
    try:
        marathons = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        marathons = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        marathons = paginator.page(paginator.num_pages)
    return render(request, 'marathons/marathon_list.html', {'marathons': marathons, 'marathonDistance': marathonDistance})

def create_distance(request):
    if request.method == 'POST':
        form = MarathonDistanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('distance_list')
    else:
        form = MarathonDistanceForm()
    return render(request, 'marathons/create_distance.html', {'form': form})

def edit_distance(request, distance_id):
    distance = get_object_or_404(MarathonDistance, pk=distance_id)
    if request.method == 'POST':
        form = MarathonDistanceForm(request.POST, instance=distance)
        if form.is_valid():
            form.save()
            return redirect('distance_list')
    else:
        form = MarathonDistanceForm(instance=distance)
    return render(request, 'marathons/edit_distance.html', {'form': form, 'distance': distance})

def distance_list(request):
    distances = MarathonDistance.objects.all()
    return render(request, 'marathons/distance_list.html', {'distances': distances})

def delete_distance(request, distance_id):
    distance = get_object_or_404(MarathonDistance, pk=distance_id)
    if request.method == 'POST':
        distance.delete()
        return redirect('distance_list')
    return render(request, 'marathons/delete_distance.html', {'distance': distance})


@login_required
def create_marathon(request):
    if request.method == 'POST':
        form = MarathonForm(request.POST, request.FILES)
        if form.is_valid():
            marathon = form.save(commit=False)
            marathon.author = request.user
            marathon.save()
            # Дополнительные действия, если необходимо
            return redirect('marathons:marathon_list')
    else:
        form = MarathonForm()
    return render(request, 'marathons/create_marathon.html', {'form': form})

@login_required
def register_for_marathon(request, marathon_id):
    marathon = get_object_or_404(Marathon, pk=marathon_id)

    if request.method == 'POST':
    # Предположим, что у вас есть доступ к текущему пользователю через request.user
        user_profile = request.user.profile  # Подставьте свой способ получения профиля пользователя

        # Проверьте, не зарегистрирован ли пользователь уже на этот марафон
        if not Participant.objects.filter(user_profile=user_profile, marathon=marathon).exists():
            participant = Participant(user_profile=user_profile, marathon=marathon)
            participant.save()
            # Дополнительные действия, например, отправка уведомления пользователю
        else:
            return JsonResponse({'success': False, 'message': 'Вы уже зарегистрировались на марафон'})
            # Пользователь уже зарегистрирован на марафон, обработайте это событие по вашему усмотрению

    return render(request, 'marathons/marathon_detail.html', {'marathon': marathon})

@login_required
def marathon_detail(request, marathon):
    marathonDistance = MarathonDistance.objects.all()
    marathon = get_object_or_404(Marathon, status=Marathon.Status.PUBLISHED, slug=marathon)
    return render(request, 'marathons/marathon_detail.html', {'marathon': marathon, 'marathonDistance': marathonDistance})

