from django.shortcuts import render, redirect, reverse
from django.views.generic.edit import FormView
from django.contrib.auth.tokens import default_token_generator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from builds.utils import sort_builds_users, sort_builds_users_public
from builds.models import Builds
from .utils import signup_email, deactivate_email
from .forms import UserLoginForm, UserRegisterForm, Profile, PasswordResetForm

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
                signup_email(request)
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

@login_required
def delete_account(request):
    try:
        user = User.objects.get(id=request.user.id)
        try:
            builds = Builds.objects.filter(author=user)
        except Builds.DoesNotExist:
            builds = False
        if builds:
            for b in builds:
                if b.exterior_parts.count() > 0:
                    for item in b.exterior_parts.all():
                        item.delete()
                if b.engine_parts.count() > 0:        
                    for item in b.engine_parts.all():
                        item.delete()
                if b.running_gear_parts.count() > 0:
                    for item in b.running_gear_parts.all():
                        item.delete()
                if b.interior_parts.count() > 0:
                    for item in b.interior_parts.all():
                        item.delete()
        user.delete()
        messages.success(request, 'Account Deactivated. If you wish to create new builds you will have to re-register.')
        deactivate_email(request)
        return redirect('home')
    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('settings')
    except Exception as e:
        messages.error(request, message=e)
        return redirect('settings')

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

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'