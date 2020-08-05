from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from builds.utils import sort_builds_users, sort_builds_users_public
from .forms import UserLoginForm, UserRegisterForm, Profile

def login(request):
    """Logs a user in / display login page"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')
            else:
                login_form.add_error(
                    None,
                    "Your username or password are incorrect"
                )
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})

@login_required
def logout(request):
    """Log user out"""
    auth.logout(request)
    messages.success(request, "You have successfully been logged out.")
    return redirect(reverse('login'))

def register(request):
    """register user"""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()

            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered.")
                return redirect('home')
            else:
                messages.error(request, "Unable to register account.")
    else:
        register_form = UserRegisterForm()

    return render(request, 'register.html', {'register_form': register_form})

@login_required
def change_password(request):
    """Displays Change Password Page / Changes password in DB"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password has been updated')
            return redirect('settings')
        else:
            messages.error(request, 'There was an error with the Change Password Form.')
            return redirect('settings')

@login_required
def update_profile(request):
    """update Profile"""
    if request.method == "POST":
        form = Profile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated")
            return redirect('settings')

@login_required
def settings(request):
    """Account settings"""
    password_form = PasswordChangeForm(request.user)
    profile_form = Profile(instance=request.user)

    context = {
        'change_password_form': password_form,
        'profile_form': profile_form
    }

    return render(request, "settings.html", context)

def users_builds(request, username):
    """All of a users build"""
    sort_options = request.GET.get('sort_options')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "That user doesn't exist.")
        return redirect('builds')
    if request.user.id == user.id:
        builds = sort_builds_users(user, sort_options)
    else:
        builds = sort_builds_users_public(user, sort_options)

    paginator = Paginator(builds, 15)
    page = request.GET.get('page')
    builds_paginator = paginator.get_page(page)

    return render(request, "my_builds.html", {"builds": builds_paginator,
                                              'user': user})
