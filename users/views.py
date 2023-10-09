from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm, UserProfileEditForm, CustomUserCreationForm
from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Создаем UserProfile для пользователя
            profile = UserProfile(user=user)
            profile.save()
            
            # Выполняем вход пользователя
            login(request, user)
            
            # Редирект на страницу профиля пользователя
            return redirect('users:profile')  # Замените на ваш URL-шаблон профиля пользователя
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    user_profile = request.user.userprofile  # Получите профиль пользователя
    form = UserProfileEditForm(instance=user_profile)
    return render(request, 'profile/profile.html', {'user_profile': user_profile, 'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Вход успешен
            login(request, user)
            return JsonResponse({'success': True})
        else:
            # Неверные учетные данные
            return JsonResponse({'success': False, 'error_message': 'Неверные учетные данные'})

    # Если это не POST-запрос, вернуть ошибку
    return JsonResponse({'success': False, 'error_messageeeeee': 'Метод запроса не поддерживается'})

def logout_view(request):
    logout(request)
    return redirect('marathons:marathon_list')



@login_required
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')  # Перенаправьте пользователя на страницу профиля после редактирования
    else:
        form = ProfileForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'profile/edit_profile.html', context)