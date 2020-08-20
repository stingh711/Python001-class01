from django.shortcuts import render
from django.http import HttpResponseRedirect
from login.forms import LoginForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            auth.login(request, user)
            return HttpResponseRedirect(reverse("welcome"))
    else:
        form = LoginForm()
    return render(request, "login/login.html", {"form": form})


@login_required
def welcome(request):
    username = request.user.username
    return render(request, "login/welcome.html", {"username": username})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse("login"))
