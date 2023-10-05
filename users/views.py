from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:profile')  # Перенаправить на страницу входа после успешной регистрации
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    # Получите профиль пользователя, связанный с текущим пользователем
    user_profile = UserProfile.objects.get(user=request.user)

    context = {'user_profile': user_profile}
    return render(request, 'profile/profile.html', context)

@login_required
def edit_profile(request):
    user_profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile')  # Перенаправьте пользователя на страницу профиля после редактирования
    else:
        form = ProfileForm(instance=user_profile)

    context = {'form': form}
    return render(request, 'profile/edit_profile.html', context)