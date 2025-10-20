from django.contrib import messages
from django.contrib.auth import login, logout as auth_logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import SignupForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account created. Welcome to Magma7Fitness!')
            login(request, user)
            return redirect('memberships:dashboard')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {"form": form})


def logout_view(request):
    """Log the user out and redirect to home (or safe 'next')."""
    next_url = request.GET.get('next') or request.POST.get('next')
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('core:home')
