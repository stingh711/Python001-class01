from django.urls import path
from django.contrib.auth import views as auth_view

from . import views


urlpatterns = [
    # path("login/", views.login, name="login"),
    # path("logout/", views.logout, name="logout"),
    path(
        "login/",
        auth_view.LoginView.as_view(template_name="login/login.html"),
        name="login",
    ),
    path("logout/", auth_view.LogoutView.as_view(next_page="login"), name="logout"),
    path("welcome/", views.welcome, name="welcome"),
]
