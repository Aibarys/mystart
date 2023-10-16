from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Marathon, Participation, MarathonDistance, Distance
from .forms import MarathonForm, Marathon, SearchForm, DistancePriceForm, ParticipateForm
from .filters import MarathonFilter
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.forms import formset_factory

def marathon_list(request):
    marathon_list = Marathon.published.all()
    marathonDistance = MarathonDistance.objects.all()
    paginator = Paginator(marathon_list, 6) 
    page_number = request.GET.get('page', 1)
    form = SearchForm() 
    query = None
    results = []
    filter = MarathonFilter(request.GET, queryset=Marathon.published.all())
    print(request.GET, filter.qs)

    if 'query' in request.GET:
        form = SearchForm(request.GET) 
        if form.is_valid():
            query = form.cleaned_data['query'] 
            results = Marathon.published.annotate( search=SearchVector('title', 'description'), ).filter(search=query)
    
    try:
        marathons = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        marathons = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        marathons = paginator.page(paginator.num_pages)
    return render(request, 'marathons/marathon_list.html', {'marathons': marathons, 
                                                            'marathonDistance': marathonDistance, 
                                                            'form': form, 
                                                            'query': query, 
                                                            'results': results, 
                                                            'filter': filter})

@login_required
def create_marathon(request):
    print(request.POST)
    if request.method == 'POST':
        form = MarathonForm(request.POST, request.FILES)
        distances_and_prices = formset_factory(DistancePriceForm)(request.POST)
        
        if form.is_valid() and distances_and_prices.is_valid():
            marathon = form.save(commit=False)
            marathon.author = request.user
            marathon.save()
            
            for distance_price_form in distances_and_prices:
                if distance_price_form.is_valid():
                    distance = distance_price_form.cleaned_data['distance']
                    price = distance_price_form.cleaned_data['price']
                    marathon_distance = MarathonDistance(marathon=marathon, distance=distance, price=price)
                    marathon_distance.save()
                else:
                    # Выведите ошибки формы, чтобы понять, в чём проблема.
                    print("Form errors:", distance_price_form.errors)

            return redirect('marathons:marathon_list')
    else:
        form = MarathonForm()
        DistancePriceFormset = formset_factory(DistancePriceForm, extra=1)
        distances_and_prices = DistancePriceFormset()



    return render(request, 'marathons/create_marathon.html', {'form': form, 'distances_and_prices': distances_and_prices})

@login_required
def register_for_marathon(request, marathon_id):
    marathon = get_object_or_404(Marathon, pk=marathon_id)

    if request.method == 'POST':
    # Предположим, что у вас есть доступ к текущему пользователю через request.user
        user_profile = request.user.profile  # Подставьте свой способ получения профиля пользователя

        # Проверьте, не зарегистрирован ли пользователь уже на этот марафон
        if not Participation.objects.filter(user_profile=user_profile, marathon=marathon).exists():
            participant = Participation(user_profile=user_profile, marathon=marathon)
            participant.save()
            # Дополнительные действия, например, отправка уведомления пользователю
        else:
            return JsonResponse({'success': False, 'message': 'Вы уже зарегистрировались на марафон'})
            # Пользователь уже зарегистрирован на марафон, обработайте это событие по вашему усмотрению

    return render(request, 'marathons/marathon_detail.html', {'marathon': marathon})

def marathon_detail(request, marathon):
    marathonDistance = MarathonDistance.objects.all()
    distances = MarathonDistance.objects.filter(marathon=marathon)
    marathon = get_object_or_404(Marathon, status=Marathon.Status.PUBLISHED, slug=marathon)
    
    form = ParticipateForm()
    if request.method == "POST":
        form = ParticipateForm(request.POST)
        if form.is_valid():
            # TODO: сохраните информацию о участии и перенаправьте на страницу подтверждения или оплаты
            pass
    return render(request, 'marathons/marathon_detail.html', {'marathon': marathon, 
                                                              'marathonDistance': marathonDistance, 
                                                              'distances': distances, 
                                                              'form': form})


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

@login_required
def participate_in_marathon(request, marathon_slug, distance_id):
    marathon = get_object_or_404(Marathon, slug=marathon_slug)
    distance = get_object_or_404(MarathonDistance, id=distance_id)
    
    # Проверяем, не участвует ли пользователь уже в этом марафоне
    if Participation.objects.filter(user_profile=request.user.profile, marathon=marathon).exists():
        # Перенаправляем на другую страницу или показываем сообщение об ошибке
        pass 
    else:
        Participation.objects.create(user_profile=request.user.profile, marathon=marathon)
        # Перенаправляем на страницу оплаты или показываем сообщение о успешном участии
        pass

    return redirect('marathons:marathon_list')