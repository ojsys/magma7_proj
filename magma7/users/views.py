from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render

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

