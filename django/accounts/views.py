from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, SignupForm


def landing_view(request):
    return render(request, 'landing.html')


@login_required
def home(request):
    return render(request, 'accounts/home.html')


@login_required
def profile_view(request):
    form = ProfileUpdateForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your profile details were saved successfully.')
        return redirect('profile')
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def reset_user_data(request):
    if request.method == 'POST':
        request.user.reports.all().delete()
        request.user.conversations.all().delete()
        messages.warning(request, 'Your saved report and chat data has been reset.')
        return redirect('profile')
    return redirect('profile')


def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('login')
    return redirect('home')
