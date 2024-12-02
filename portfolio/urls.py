from django.urls import path
from . import views

urlpatterns = [
    path('', views.public_portfolio, name='public_portfolio'),
]