from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.painel, name="painel"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="obras/login.html"
        ),
        name="login",
    ),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("obras/nova/", views.nova_obra, name="nova_obra"),

    path(
        "obras/<int:obra_id>/",
        views.detalhe_obra,
        name="detalhe_obra",
    ),

    path(
        "obras/<int:obra_id>/lancamentos/novo/",
        views.novo_lancamento,
        name="novo_lancamento",
    ),

    path(
        "lancamentos/<int:lancamento_id>/editar/",
        views.editar_lancamento,
        name="editar_lancamento",
    ),
]
