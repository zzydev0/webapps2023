from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from sign import models
from sign.forms import RegisterForm, LoginForm
from sign.models import User
from util.convert import convert


# Create your views here.


def index(request):
    pass
    return render(request, 'sign/index.html')


def register(request):
    if request.method == 'POST':
        # get the form
        register_form = RegisterForm(request.POST)
        message = ''
        # validate the form
        if register_form.is_valid():
            # get info
            username = register_form.cleaned_data['username']
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            confirmed_password = register_form.cleaned_data['confirmed_password']
            currency = register_form.cleaned_data['currency']
            # two inputs of password must agree
            if password != confirmed_password:
                message = 'Two passwords are disagree.'
                return render(request, 'sign/register.html', locals())
            else:
                # username must be unique
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:
                    message = 'The username has been registered.'
                    return render(request, 'sign/register.html', locals())
                # email must be unique
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = 'The email has been registered.'
                    return render(request, 'sign/register.html', locals())
                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    currency=currency,
                    balance=convert('http://3.88.160.124:8000', 'GBP', currency, 1000)
                )
                auth.login(request, new_user)
                return render(request, 'sign/info.html', locals())
    register_form = RegisterForm()
    return render(request, 'sign/register.html', locals())


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        message = ''
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user_obj = authenticate(username=username, password=password)
            if user_obj is not None:
                auth.login(request, user_obj)
                return redirect('/sign/profile')
            else:
                message = "Wrong username or password."
        return render(request, 'sign/login.html', locals())
    login_form = LoginForm()
    return render(request, 'sign/login.html', locals())


@login_required(login_url='/sign/login/')
def profile(request):
    curr_user = models.User.objects.get(username=request.user)
    return render(request, 'sign/profile.html', locals())


def logout(request):
    auth.logout(request)
    return redirect('/sign/')
